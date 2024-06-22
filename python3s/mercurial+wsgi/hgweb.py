#!/usr/bin/python3
#
from mercurial import demandimport
from mercurial.hgweb.hgwebdir_mod import hgwebdir, wsgicgi
import os.path
import os
from basic_auth_middleware import BaseAuth, parse

os.environ["HGENCODING"] = "UTF-8"

demandimport.enable()


class localauth(BaseAuth):
    def authenticate(self, env: dict[str, str]):
        parsed = parse(env.get("HTTP_AUTHORIZATION", ""))
        if not parsed:
            return False
        # print(parsed)
        env.update({"REMOTE_USER": parsed[0]})
        return True


configpath = os.path.dirname(__file__)+"/hgweb.ini"
application = localauth(hgwebdir(configpath.encode()))


# print(dir(app))
if __name__ == "__main__":
    wsgicgi.launch(application)
