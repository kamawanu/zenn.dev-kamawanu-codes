#!python3.8

import sys
from typing import Dict, List
import glob
import os.path
import time
import subprocess
import shutil


class anydir(object):
    root: str = None
    files: set = None

    def __init__(self, root, files):
        self.root = root
        self.files = set(files)


REPO: Dict[str, List[anydir]] = dict()


def sglob(root: str) -> List[str]:
    ln = len(root)+1
    return [xx[ln:] for xx in glob.iglob(root+"/**")]


_ROOTQUE_ = sys.argv[1:]
# print(ROOTQ)
while len(_ROOTQUE_) > 0:
    _root_ = _ROOTQUE_[0]
    _ROOTQUE_ = _ROOTQUE_[1:]
    print(len(_ROOTQUE_), _root_, _ROOTQUE_[:3], )

    allfiles = sglob(_root_)
    dironly = [xx for xx in allfiles if os.path.isdir(
        _root_+"/"+xx) and xx != "." and xx != ".."]
    fileonly = [xx for xx in allfiles if os.path.isfile(_root_+"/"+xx)]

    ##print(dironly)

    if (".hg" in dironly) or (".git" in dironly) or (".svn" in dironly):
        continue

    if len(allfiles) == len(dironly):
        continue

    print(len(_ROOTQUE_), _root_, len(allfiles), _ROOTQUE_[:3], )

    # print(dironly)
    # print(fileonly)
    for d1 in dironly:
        if d1[0] == "." or d1[0] == "^":
            continue
        _newer = anydir(_root_ + "/" + d1, [])
        if not d1 in REPO:
            REPO.update({d1: [_newer]})
        else:
            if len(REPO[d1]) > 1:
                assert REPO[d1][-1].root != d1
            REPO[d1].append(_newer)
        # print(REPO[d1])
        if len(REPO[d1]) > 1:
            r1 = REPO[d1][0].root
            r2 = REPO[d1][-1].root
            l1 = set(sglob(r1))
            l2 = set(sglob(r2))
            _c = l1 & l2
            _s = l1 ^ l2
            print(d1, r1, len(l1), r2, len(l2), len(_c), len(_s))
            assert os.path.isdir(r1) and os.path.isdir(r2)

            if len(_c) == 0:
                for f1 in l2:
                    os.rename(r2 + "/" + f1, r1 + "/" + f1)
                if os.path.isdir(r1+"/.hg") and os.path.isdir(r2+"/.hg"):
                    subprocess.run(["hg", "-R", r1, "pull", r2])
                    shutil.rmtree(r2+"/.hg")
                os.rmdir(r2)
            elif len(_c) > 3 or len(_s) == 0:
                os.rename(r2, r1 + "/^%f" % time.time())

            ##raise Exception("DEBUGGING")
        _ROOTQUE_.append(_root_+"/"+d1)
print(REPO)
