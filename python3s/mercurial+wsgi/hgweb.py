#!/usr/local/bin/python3.12
#
from mercurial import demandimport
from mercurial.hgweb.hgwebdir_mod import hgwebdir, wsgicgi
from mercurial.hgweb.request import wsgiapplication
import os.path
import os
from basic_auth_middleware import BaseAuth, parse

os.environ["HGENCODING"] = "UTF-8"

demandimport.enable()


class localauth(BaseAuth):
    def authenticate(self, env):
        parsed = parse(env.get("HTTP_AUTHORIZATION", ""))
        if not parsed:
            return False
        print(parsed)
        env.update({"REMOTE_USER": parsed[0]})
        return True


def make_web_app():
    configpath = os.path.dirname(__file__)+"/hgweb.ini"
    return localauth(hgwebdir(configpath.encode()))


application = wsgiapplication(make_web_app)

# print(dir(app))
if __name__ == "__main__":
    wsgicgi.launch(make_web_app())
