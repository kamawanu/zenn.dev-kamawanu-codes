#!/usr/local/bin/python3.12
#
from mercurial import demandimport
from mercurial.hgweb.hgwebdir_mod import hgwebdir, wsgicgi
from mercurial.hgweb.request import wsgiapplication
import os.path
import os
import dataclasses
import pprint
from gunicorn.http.wsgi import Response

os.environ["HGENCODING"] = "UTF-8"

demandimport.enable()


def make_web_app():
    configpath = os.path.dirname(__file__)+"/hgweb.ini"
    return hgwebdir(configpath.encode())


application = wsgiapplication(make_web_app)

# print(dir(app))
if __name__ == "__main__":
    wsgicgi.launch(make_web_app())
