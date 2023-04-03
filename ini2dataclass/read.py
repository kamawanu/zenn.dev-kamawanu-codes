import dataclasses

@dataclasses.dataclass(kw_only=True)
class Database:
    host:str
    port:str
    username:str
    password:str
    database:str
    def __post_init__(self):
        self.port = int(self.port)

import configparser

iniread = configparser.RawConfigParser()
iniread.read("setting.ini")

cfg_database = Database(**iniread["Database"])

print(cfg_database)
