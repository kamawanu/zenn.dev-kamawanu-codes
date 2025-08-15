import mysql.connector
from typing import Dict, List, Optional, Any, Union
import re
from collections import defaultdict


class MySQLConfigParser:
    """
    configparser.RawConfigParserの互換インターフェースを提供し、
    バックエンドでMySQLに接続するクラス
    """
    
    def __init__(self, host: str = 'localhost', user: str = 'root', 
                 password: str = '', database: str = 'config_db', 
                 table: str = 'config', port: int = 3306):
        """
        Args:
            host: MySQLホスト
            user: MySQLユーザー名
            password: MySQLパスワード
            database: データベース名
            table: テーブル名 (section, key, valueカラムを持つ)
            port: MySQLポート
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.table = table
        self.port = port
        self._connection = None
        self._connect()
    
    def _connect(self):
        """MySQLに接続"""
        try:
            self._connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                autocommit=True
            )
        except mysql.connector.Error as e:
            raise ConnectionError(f"MySQL接続エラー: {e}")
    
    def _ensure_connection(self):
        """接続が有効か確認し、必要に応じて再接続"""
        if not self._connection or not self._connection.is_connected():
            self._connect()
    
    def _execute_query(self, query: str, params: Optional[tuple] = None) -> List[tuple]:
        """SQLクエリを実行して結果を返す"""
        self._ensure_connection()
        cursor = self._connection.cursor()
        try:
            cursor.execute(query, params or ())
            return cursor.fetchall()
        finally:
            cursor.close()
    
    def _execute_update(self, query: str, params: Optional[tuple] = None):
        """更新系SQLクエリを実行"""
        self._ensure_connection()
        cursor = self._connection.cursor()
        try:
            cursor.execute(query, params or ())
        finally:
            cursor.close()
    
    def sections(self) -> List[str]:
        """セクション一覧を取得"""
        query = f"SELECT DISTINCT section FROM {self.table} ORDER BY section"
        results = self._execute_query(query)
        return [row[0] for row in results]
    
    def has_section(self, section: str) -> bool:
        """セクションが存在するかチェック"""
        query = f"SELECT COUNT(*) FROM {self.table} WHERE section = %s"
        results = self._execute_query(query, (section,))
        return results[0][0] > 0
    
    def add_section(self, section: str):
        """セクションを追加（実際にはキーが追加されるまで何もしない）"""
        if self.has_section(section):
            raise ValueError(f"Section '{section}' already exists")
        # MySQLベースなので、実際にキーが追加されるまでセクションは作成されない
    
    def remove_section(self, section: str) -> bool:
        """セクションとその中身を削除"""
        if not self.has_section(section):
            return False
        query = f"DELETE FROM {self.table} WHERE section = %s"
        self._execute_update(query, (section,))
        return True
    
    def options(self, section: str) -> List[str]:
        """指定セクションのオプション（キー）一覧を取得"""
        query = f"SELECT key FROM {self.table} WHERE section = %s ORDER BY key"
        results = self._execute_query(query, (section,))
        return [row[0] for row in results]
    
    def has_option(self, section: str, option: str) -> bool:
        """セクション内にオプションが存在するかチェック"""
        query = f"SELECT COUNT(*) FROM {self.table} WHERE section = %s AND key = %s"
        results = self._execute_query(query, (section, option))
        return results[0][0] > 0
    
    def get(self, section: str, option: str, fallback: Optional[str] = None) -> str:
        """指定セクション・オプションの値を取得"""
        query = f"SELECT value FROM {self.table} WHERE section = %s AND key = %s"
        results = self._execute_query(query, (section, option))
        
        if not results:
            if fallback is not None:
                return fallback
            raise KeyError(f"Option '{option}' in section '{section}' not found")
        
        return results[0][0]
    
    def getint(self, section: str, option: str, fallback: Optional[int] = None) -> int:
        """値を整数として取得"""
        try:
            value = self.get(section, option)
            return int(value)
        except (ValueError, KeyError):
            if fallback is not None:
                return fallback
            raise
    
    def getfloat(self, section: str, option: str, fallback: Optional[float] = None) -> float:
        """値を浮動小数点数として取得"""
        try:
            value = self.get(section, option)
            return float(value)
        except (ValueError, KeyError):
            if fallback is not None:
                return fallback
            raise
    
    def getboolean(self, section: str, option: str, fallback: Optional[bool] = None) -> bool:
        """値をブール値として取得"""
        try:
            value = self.get(section, option).lower()
            if value in ('1', 'yes', 'true', 'on'):
                return True
            elif value in ('0', 'no', 'false', 'off'):
                return False
            else:
                raise ValueError(f"Invalid boolean value: {value}")
        except (ValueError, KeyError):
            if fallback is not None:
                return fallback
            raise
    
    def set(self, section: str, option: str, value: str):
        """値を設定（INSERT OR UPDATE）"""
        value_str = str(value)
        
        # 既存チェック
        if self.has_option(section, option):
            query = f"UPDATE {self.table} SET value = %s WHERE section = %s AND key = %s"
            self._execute_update(query, (value_str, section, option))
        else:
            query = f"INSERT INTO {self.table} (section, key, value) VALUES (%s, %s, %s)"
            self._execute_update(query, (section, option, value_str))
    
    def remove_option(self, section: str, option: str) -> bool:
        """オプションを削除"""
        if not self.has_option(section, option):
            return False
        query = f"DELETE FROM {self.table} WHERE section = %s AND key = %s"
        self._execute_update(query, (section, option))
        return True
    
    def items(self, section: str) -> List[tuple]:
        """セクション内の全アイテム（キー・値ペア）を取得"""
        query = f"SELECT key, value FROM {self.table} WHERE section = %s ORDER BY key"
        results = self._execute_query(query, (section,))
        return [(row[0], row[1]) for row in results]
    
    def read(self, filenames: Union[str, List[str]]):
        """ファイル読み込み（互換性のため空実装）"""
        # MySQLベースなので何もしない
        pass
    
    def read_file(self, fp):
        """ファイルオブジェクトから読み込み（互換性のため空実装）"""
        # MySQLベースなので何もしない
        pass
    
    def read_string(self, string: str):
        """文字列から設定を読み込み（互換性のため空実装）"""
        # MySQLベースなので何もしない
        pass
    
    def write(self, fp):
        """設定をファイルに書き出し"""
        sections = self.sections()
        for section in sections:
            fp.write(f"[{section}]\n")
            for key, value in self.items(section):
                fp.write(f"{key} = {value}\n")
            fp.write("\n")
    
    def __getitem__(self, section: str):
        """dict風インターフェース：config[section]"""
        return MySQLSection(self, section)
    
    def __contains__(self, section: str) -> bool:
        """'section' in config の実装"""
        return self.has_section(section)
    
    def close(self):
        """MySQL接続を閉じる"""
        if self._connection and self._connection.is_connected():
            self._connection.close()
    
    def __del__(self):
        """デストラクタで接続を閉じる"""
        self.close()


class MySQLSection:
    """
    セクション用のdict風インターフェース
    config[section][key] のような使い方を可能にする
    """
    
    def __init__(self, config: MySQLConfigParser, section: str):
        self.config = config
        self.section = section
    
    def __getitem__(self, key: str) -> str:
        return self.config.get(self.section, key)
    
    def __setitem__(self, key: str, value: str):
        self.config.set(self.section, key, str(value))
    
    def __contains__(self, key: str) -> bool:
        return self.config.has_option(self.section, key)
    
    def __delitem__(self, key: str):
        if not self.config.remove_option(self.section, key):
            raise KeyError(f"Option '{key}' not found in section '{self.section}'")
    
    def get(self, key: str, fallback: Optional[str] = None) -> str:
        return self.config.get(self.section, key, fallback)
    
    def items(self):
        return self.config.items(self.section)
    
    def keys(self):
        return self.config.options(self.section)


# 使用例
if __name__ == "__main__":
    # 使用例
    config = MySQLConfigParser(
        host='localhost',
        user='your_user',
        password='your_password',
        database='config_db',
        table='config'
    )
    
    # configparser.RawConfigParserと同じように使える
    try:
        # セクション作成・値設定
        config.set('database', 'host', 'localhost')
        config.set('database', 'port', '3306')
        config.set('database', 'user', 'admin')
        
        # 値の取得
        host = config.get('database', 'host')
        port = config.getint('database', 'port')
        
        # dict風アクセス
        config['api'] = {}  # セクション作成的な使い方
        config.set('api', 'endpoint', 'https://api.example.com')
        endpoint = config['api']['endpoint']
        
        print(f"Database: {host}:{port}")
        print(f"API Endpoint: {endpoint}")
        
        # セクション一覧
        print("Sections:", config.sections())
        
        # セクション内のアイテム
        print("Database items:", config.items('database'))
        
    finally:
        config.close()