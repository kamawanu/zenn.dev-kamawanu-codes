import dataclasses

@dataclasses.dataclass(kw_only=True)
class Database:
    host:str
    port:str
    username:str
    password:str
    database:str

import configparser

iniread = configparser.RawConfigParser()
iniread.read("setting.ini")

cfg_database = Database(**iniread["Database"])

print(cfg_database)
