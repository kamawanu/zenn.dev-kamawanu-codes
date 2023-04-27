#!/usr/bin/python3
from mercurial import registrar, commands, ui, hg
from mercurial.utils import urlutil
###from mercurial.i18n import _
import os.path
import os
import fnmatch
from typing import Tuple, Any, Iterable

cmdtable = {}
command = registrar.command(cmdtable)


def isurl(url: str) -> bool:
    return fnmatch.fnmatch("http*://*", url)


def _e(v: str) -> bytes:
    return v.encode("utf8")


def _d(v: bytes) -> str:
    return v.decode("utf8")


def digrepo(parentui, parentrepo, fn1: str, url: str = None):
    fn1_f = os.path.realpath(fn1)

    assert parentrepo.root in _e(os.path.realpath(fn1))
    ##print(fn1_f_ll, roottkn)

    def tryrepo() -> Iterable[Tuple[str, bool, bool, Any]]:
        roottkn = parentrepo.root.decode("utf8").split("/")
        fn1_f_ll = fn1_f.split("/")
        for ll in range(len(roottkn), len(fn1_f_ll)):
            _ccdn = "/".join(fn1_f_ll[:ll])
            yield (
                _ccdn, os.path.isdir(_ccdn), os.path.isfile(_ccdn),
                os.path.isdir(_ccdn + "/.hg") and hg.repository(parentui, _e(_ccdn))  # COALESCE
            )

    tryrepodn_ll = [n for n in tryrepo()]
    ###print(tryrepodn_ll)
    assert tryrepodn_ll[0][3]
    near_repo_ll = [n for n in tryrepodn_ll if n[3]]
    assert near_repo_ll[-1][3]
    ###print(near_repo_ll[-1][3])

    pathleft = fn1_f.replace(_d(parentrepo.root) + "/", "")
    for d1 in tryrepodn_ll:
        if not os.path.isdir(d1[0]):
            os.mkdir(d1[0])
    h1repo = near_repo_ll[-1]
    ####print(pathleft, h1repo[3].root)

    ###pathleft, h1repo = digdir(parentrepo, fn1)

    if url is None:
        commands.init(parentui, dest=_e(fn1_f))
    else:
        _peer = hg.peer(parentui, {}, _e(url) )
        commands.clone(parentui, _peer, dest=_e(fn1_f) )

    hs = open(h1repo[0] + "/.hgsub", "a")
    hs.write("%s=%s\n" % (pathleft, url or pathleft))
    hs.close()

    if not b".hgsub" in h1repo[3][None]:
        commands.add(parentui, h1repo[3], b".hgsub")
    commands.add(parentui, h1repo[3], _e(pathleft))
    commands.commit(parentui, parentrepo,
                    message=_e("subrepo %s added " % pathleft), subrepos=True)

    ###addsub(h1repo, parentui, pathleft)


@command(b'addsubrepo', [])
def addsubrepo(ui, parentrepo, *args):
    ###import pdb
    # pdb.set_trace()
    ###print(args)

    if len(args) == 1:
        fn = args[0]
        if not isurl(_d(fn)):
            digrepo(ui, parentrepo, _d(fn))
        pass
    elif len(args) == 2:
        digrepo(ui, parentrepo, _d(args[0]), _d(args[1]))
    else:
        pass
