#!/bin/bash -ex

for HGD in $( find . -mindepth 3 -type d -name .hg -printf "%h " )
do
    RID=$(
        cd "$HGD"
        hg id -r 0 || exit 9
    ) || continue
    RID=$( echo $RID | awk '{print $1}' )
    BN=$( basename $HGD )
    LOCALDIR=hg-$RID-$BN
    if [ \! -d $LOCALDIR ]
    then
        mv -f $HGD $LOCALDIR
        ###break
    fi
done
