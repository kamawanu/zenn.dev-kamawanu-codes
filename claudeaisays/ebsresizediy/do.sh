#!/bin/bash
# ebs_auto_expand.sh
# 条件: 残量10%以下 or 50GB未満 → 50GB増量
# 想定: パーティションごとに別EBSボリューム、FS=xfs or ext4
# cron推奨: 1日1回程度（EBS modify-volumeは6時間以内に同一ボリューム2回不可）

set -euo pipefail

LOG=/var/log/ebs_auto_expand.log
THRESHOLD_PCT=10   # 使用率がこれを超えたら
THRESHOLD_GB=50    # 空き容量がこれ未満なら（GB）
EXPAND_GB=50       # 増量サイズ（GB）

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') $*" | tee -a "$LOG"
}

# IDフィールド（Amazon_Elastic_Block_Store_volXXXX-partN）からvol-XXXXを抽出
# lsblk IDはハイフンなし（vol05d749a1b5f1bcd6b）→ vol-05d749a1b5f1bcd6b に変換
extract_vol_id() {
    local id="$1"
    local raw
    raw=$(echo "$id" | grep -oP 'vol[0-9a-f]+')
    [[ -z "$raw" ]] && return 1
    echo "${raw/vol/vol-}"
}

expand_volume() {
    local vol_id="$1"
    local current_gb="$2"
    local new_gb=$(( current_gb + EXPAND_GB ))

    log "  Expanding ${vol_id}: ${current_gb}GB → ${new_gb}GB"
    aws ec2 modify-volume --volume-id "$vol_id" --size "$new_gb" \
        --query 'VolumeModification.ModificationState' --output text
}

wait_for_volume() {
    local vol_id="$1"
    log "  Waiting for ${vol_id}..."
    for i in $(seq 1 30); do
        local state
        state=$(aws ec2 describe-volumes-modifications \
            --volume-ids "$vol_id" \
            --query 'VolumesModifications[0].ModificationState' \
            --output text 2>/dev/null)
        if [[ "$state" == "optimizing" || "$state" == "completed" ]]; then
            log "  Volume state: ${state}"
            return 0
        fi
        sleep 10
    done
    log "  WARNING: volume did not reach optimizing state in time"
    return 1
}

resize_fs() {
    local diskdev="$1"   # 例: /dev/nvme0n1
    local partnum="$2"   # 例: 1
    local mountpoint="$3"
    local fstype="$4"

    log "  growpart ${diskdev} ${partnum}"
    growpart "$diskdev" "$partnum" || true  # already max → exit1 but OK

    case "$fstype" in
        xfs)
            log "  xfs_growfs ${mountpoint}"
            xfs_growfs "$mountpoint"
            ;;
        ext4|ext3|ext2)
            log "  resize2fs ${diskdev}p${partnum}"
            resize2fs "${diskdev}p${partnum}"
            ;;
        *)
            log "  WARN: unknown fstype ${fstype}, skipping resize"
            ;;
    esac
}

# --- main ---

log "=== Start ==="

# lsblk -b --raw: ID SIZE PATH FSTYPE MOUNTPOINTS FSUSE%
# マウントポイントあり・FSUSEあり（＝マウント済みパーティション）のみ対象
# vfatは除外（/boot/efi等）
while IFS=' ' read -r id size path fstype mountpoint fsuse; do
    [[ "$fstype" == "vfat" ]] && continue

    vol_id=$(extract_vol_id "$id") || { log "  WARN: cannot extract vol-id from ${id}"; continue; }

    # バイト → GB
    size_gb=$(( size / 1024 / 1024 / 1024 ))

    # 空き容量・使用率はdfから（lsblkのFSUSE%は参考値なのでdfで正確に取る）
    read -r avail_gb use_pct < <(df -BG "$mountpoint" \
        | awk 'NR==2 {gsub(/G/,"",$4); gsub(/%/,"",$5); print $4, $5}')

    log "--- ${path} → ${vol_id} (${mountpoint}, ${fstype}, ${size_gb}GB total, ${avail_gb}GB avail, ${use_pct}%used)"

    # 拡張判定
    need_expand=0
    if [ "$use_pct" -ge $(( 100 - THRESHOLD_PCT )) ]; then
        log "  Trigger: usage ${use_pct}% >= $(( 100 - THRESHOLD_PCT ))%"
        need_expand=1
    elif [ "$avail_gb" -lt "$THRESHOLD_GB" ]; then
        log "  Trigger: avail ${avail_gb}GB < ${THRESHOLD_GB}GB"
        need_expand=1
    fi

    if [ "$need_expand" -eq 0 ]; then
        log "  OK, skipping."
        continue
    fi

    # 親ディスクのデバイスとパーティション番号
    # /dev/nvme0n1p1 → diskdev=/dev/nvme0n1, partnum=1
    # /dev/sda1      → diskdev=/dev/sda,     partnum=1
    partnum=$(echo "$path" | grep -oP '\d+$')
    diskdev="${path%${partnum}}"
    # nvme系は末尾が "p1" なので 'p' も除去
    diskdev="${diskdev%p}"

    # EBS拡張
    if ! expand_volume "$vol_id" "$size_gb"; then
        log "  ERROR: modify-volume failed for ${vol_id}"
        continue
    fi

    # 反映待ち
    if ! wait_for_volume "$vol_id"; then
        log "  ERROR: volume not ready, skipping fs resize"
        continue
    fi

    # FS拡張
    resize_fs "$diskdev" "$partnum" "$mountpoint" "$fstype"
    log "  Done: ${path} expanded."

done < <(lsblk -o ID,SIZE,PATH,FSTYPE,MOUNTPOINTS,FSUSE% -b --raw \
    | tail -n +2 \
    | awk '$5 != "" && $6 != ""')

log "=== Done ==="