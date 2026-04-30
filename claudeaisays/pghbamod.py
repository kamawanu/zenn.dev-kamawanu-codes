#!/usr/bin/env python3
"""
pg_hba.conf 安全更新スクリプト
PostgreSQLのpg_hba.confファイルに新しいエントリを安全に追加します
"""

import argparse
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path


class PgHbaUpdater:
    VALID_TYPES = ['local', 'host', 'hostssl', 'hostnossl', 'hostgssenc', 'hostnogssenc']
    VALID_METHODS = ['trust', 'reject', 'scram-sha-256', 'md5', 'password', 'gss', 
                     'sspi', 'ident', 'peer', 'ldap', 'radius', 'cert', 'pam', 'bsd']
    
    def __init__(self, config_dir):
        self.config_dir = Path(config_dir)
        self.config_file = self.config_dir / 'pg_hba.conf'
        
    def validate_inputs(self, conn_type, database, user, address, method):
        """入力値のバリデーション"""
        errors = []
        
        # タイプの検証
        if conn_type not in self.VALID_TYPES:
            errors.append(f"無効なタイプ: {conn_type}. 有効な値: {', '.join(self.VALID_TYPES)}")
        
        # localタイプの場合はアドレス不要
        if conn_type == 'local' and address:
            errors.append("タイプ'local'の場合、アドレスは指定できません")
        
        # それ以外のタイプではアドレス必須
        if conn_type != 'local' and not address:
            errors.append(f"タイプ'{conn_type}'の場合、アドレスは必須です")
        
        # メソッドの検証
        if method not in self.VALID_METHODS:
            errors.append(f"無効なメソッド: {method}. 有効な値: {', '.join(self.VALID_METHODS)}")
        
        # データベースとユーザーの検証
        if not database:
            errors.append("データベース名は必須です")
        if not user:
            errors.append("ユーザー名は必須です")
        
        return errors
    
    def create_backup(self):
        """設定ファイルのバックアップを作成"""
        if not self.config_file.exists():
            raise FileNotFoundError(f"設定ファイルが見つかりません: {self.config_file}")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = self.config_file.parent / f'pg_hba.conf.backup_{timestamp}'
        
        shutil.copy2(self.config_file, backup_file)
        print(f"バックアップを作成しました: {backup_file}")
        return backup_file
    
    def format_entry(self, conn_type, database, user, address, method):
        """pg_hba.confのエントリをフォーマット"""
        if conn_type == 'local':
            # localタイプの場合はアドレスなし
            return f"{conn_type:<15} {database:<15} {user:<15} {method}"
        else:
            # それ以外はアドレスあり
            return f"{conn_type:<15} {database:<15} {user:<15} {address:<23} {method}"
    
    def check_duplicate(self, new_entry):
        """重複エントリのチェック"""
        with open(self.config_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # コメントと空白を除去して正規化
        new_normalized = ' '.join(new_entry.split())
        
        for line in content.splitlines():
            line = line.strip()
            if line and not line.startswith('#'):
                line_normalized = ' '.join(line.split())
                if line_normalized == new_normalized:
                    return True
        return False
    
    def add_entry(self, conn_type, database, user, address, method, force=False):
        """エントリを追加"""
        # バリデーション
        errors = self.validate_inputs(conn_type, database, user, address, method)
        if errors:
            print("エラー:", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
            return False
        
        # エントリをフォーマット
        new_entry = self.format_entry(conn_type, database, user, address, method)
        
        # 重複チェック
        if not force and self.check_duplicate(new_entry):
            print("警告: 同じエントリが既に存在します", file=sys.stderr)
            print(f"  {new_entry}", file=sys.stderr)
            print("強制的に追加する場合は --force オプションを使用してください", file=sys.stderr)
            return False
        
        # バックアップ作成
        try:
            self.create_backup()
        except Exception as e:
            print(f"バックアップの作成に失敗しました: {e}", file=sys.stderr)
            return False
        
        # エントリを追加
        try:
            with open(self.config_file, 'a', encoding='utf-8') as f:
                f.write(f"\n# Added by pg_hba_updater on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"{new_entry}\n")
            
            print("エントリを追加しました:")
            print(f"  {new_entry}")
            print("\n変更を有効にするには、PostgreSQLをリロードしてください:")
            print("  sudo systemctl reload postgresql")
            print("  または: pg_ctl reload")
            return True
            
        except Exception as e:
            print(f"ファイルの書き込みに失敗しました: {e}", file=sys.stderr)
            return False


def main():
    parser = argparse.ArgumentParser(
        description='PostgreSQLのpg_hba.confに新しいエントリを安全に追加します',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # ローカル接続の設定
  %(prog)s -d /etc/postgresql/15/main -t local -D all -u postgres -m peer
  
  # ホスト接続の設定（IPv4）
  %(prog)s -d /etc/postgresql/15/main -t host -D mydb -u myuser -a 192.168.1.0/24 -m scram-sha-256
  
  # SSL接続の設定
  %(prog)s -d /etc/postgresql/15/main -t hostssl -D all -u all -a 0.0.0.0/0 -m scram-sha-256
        """
    )
    
    parser.add_argument('-d', '--directory', required=True,
                        help='pg_hba.confが存在するディレクトリ')
    parser.add_argument('-t', '--type', required=True,
                        choices=PgHbaUpdater.VALID_TYPES,
                        help='接続タイプ')
    parser.add_argument('-D', '--database', required=True,
                        help='データベース名（allで全て、sameusernameでユーザー名と同じDB）')
    parser.add_argument('-u', '--user', required=True,
                        help='ユーザー名（allで全て）')
    parser.add_argument('-a', '--address',
                        help='IPアドレス/CIDR（hostタイプの場合は必須）')
    parser.add_argument('-m', '--method', required=True,
                        choices=PgHbaUpdater.VALID_METHODS,
                        help='認証方式')
    parser.add_argument('-f', '--force', action='store_true',
                        help='重複チェックをスキップして強制的に追加')
    
    args = parser.parse_args()
    
    # 更新実行
    updater = PgHbaUpdater(args.directory)
    success = updater.add_entry(
        args.type,
        args.database,
        args.user,
        args.address,
        args.method,
        args.force
    )
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()