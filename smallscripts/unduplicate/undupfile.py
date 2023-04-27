#!python3.8

import sys
from typing import Dict, List
import glob
import os.path
import time
import subprocess
import shutil
import hashlib


def sglob(root: str) -> List[str]:
    if root[-1] == "/":
        root = root[:-1]
    print(root)
    ln = len(root)+1
    return [xx[ln:] for xx in glob.iglob(root+"/./**", recursive=True) if os.path.isfile(xx) and xx[ln:] != "./"]


REPO: Dict[str, List[str]] = dict()


ROOTQ = sys.argv[1:]
# print(ROOTQ)
# while len(ROOTQ) > 0:
root = ROOTQ[0]
ROOTQ = ROOTQ[1:]
print(root, ROOTQ[:2], len(ROOTQ))
###ncrop = len(root)+1
allfiles = sglob(root)
# print(allfiles)
print(len(allfiles))
for f1 in allfiles:
    d = root + "/" + os.path.dirname(f1)
    fo = os.path.basename(f1)
    if not fo in REPO:
        REPO.update({fo: []})
    REPO[fo].append(d)

for bn, _paths in REPO.items():
    if len(_paths) > 1:
        xs = set()
        for p1 in _paths:
            hs = hashlib.new("md5")
            fo = open(p1+"/"+bn, "rb")
            while True:
                buf = fo.read()
                if len(buf) == 0:
                    break
                hs.update(buf)
            fo.close()
            xs.add(hs.hexdigest())
        print(bn, _paths, xs)
        if len(xs) == 1:
            for p1 in _paths[1:]:
                os.unlink(p1+"/"+bn)
