#!python3

from typing import Any


class delegate:
    t: type = None
    v: Any = None

    def __init__(self, t):
        self.t = t

    def getter(self, *args):
        return self.v

    def getgetter(self):
        return property(self.getter)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.value = self.t(args[0])


class usedelegate:
    _a = delegate(str)
    a = _a.getgetter()

    def __init__(self, **kwargs):
        cmds = {
            "a": self._a
        }
        for k, v in kwargs.items():
            if k in cmds:
                cmds[k](v)

a=usedelegate(a=1,b=2)
print(a.a)
