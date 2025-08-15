import mysql.connector
import dataclasses
import configparser
import os
from typing import Union

@dataclasses.dataclass
class wrapcursor:
    parent: "wrapmysqlapi"
    cursor: mysql.connector.cursor.MySQLCursor
    
    def execute(self, sql: str, args: Union[tuple, list] = None):
        # MySQLでは?プレースホルダーを%sに変換
        mysql_sql = sql.replace('?', '%s')
        return self.cursor.execute(mysql_sql) if not args else self.cursor.execute(mysql_sql, args)
    
    @property
    def lastrowid(self):
        return self.cursor.lastrowid
    
    def fetchone(self):
        return self.cursor.fetchone()
    
    def fetchall(self):
        return self.cursor.fetchall()

@dataclasses.dataclass
class wrapmysqlapi:
    args: list[str]
    mysql_conn: mysql.connector.MySQLConnection
    
    def cursor(self):
        return wrapcursor(self, self.mysql_conn.cursor())
    
    def commit(self):
        return self.mysql_conn.commit()
    
    def close(self):
        return self.mysql_conn.close()

def load_db_config(db_name: str, config_file: str = "db.ini"):
    """db.iniファイルから指定されたセクションの設定を読み込む"""
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"設定ファイル '{config_file}' が見つかりません")
    
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')
    
    if db_name not in config:
        raise ValueError(f"セクション '{db_name}' が設定ファイルに見つかりません")
    
    section = config[db_name]
    
    # MySQL接続パラメータを構築
    connection_params = {
        'host': section.get('host', 'localhost'),
        'port': section.getint('port', 3306),
        'database': section.get('database'),
        'user': section.get('user'),
        'password': section.get('password'),
        'charset': section.get('charset', 'utf8mb4'),
        'autocommit': section.getboolean('autocommit', False)
    }
    
    # Noneの値を除去
    connection_params = {k: v for k, v in connection_params.items() if v is not None}
    
    return connection_params

def connect(db: str, *args):
    """
    SQLite3互換のconnect関数
    dbパラメータがファイルパスの場合はそのまま、
    そうでなければdb.iniのセクション名として扱う
    """
    # ファイルパスかどうかをチェック（拡張子があるか、パス区切り文字があるかで判定）
    if '.' in db or '/' in db or '\\' in db:
        # ファイルパスの場合は従来のSQLite3として処理
        import sqlite3
        from . import sqlite_wrapper  # 元のSQLite3ラッパーをインポート
        return sqlite_wrapper.wrapsqlite3api(list(args), sqlite3.connect(db, *args))
    else:
        # セクション名の場合はMySQL接続
        config_params = load_db_config(db)
        mysql_conn = mysql.connector.connect(**config_params)
        return wrapmysqlapi(list(args), mysql_conn)

# 使用例とdb.ini設定例
"""
db.ini の設定例:

[production]
host = localhost
port = 3306
database = myapp_prod
user = prod_user
password = prod_password
charset = utf8mb4
autocommit = false

[development]
host = localhost
port = 3306
database = myapp_dev
user = dev_user
password = dev_password
charset = utf8mb4
autocommit = true

[test]
host = testserver.example.com
port = 3306
database = myapp_test
user = test_user
password = test_password

使用例:
# MySQL接続（db.iniのセクション名を指定）
conn = connect("production")

# 既存のSQLite3ファイル接続（従来通り）
conn = connect("data.db")

cursor = conn.cursor()
cursor.execute("SELECT * FROM users WHERE id = ?", (1,))
result = cursor.fetchone()
conn.commit()
conn.close()
"""