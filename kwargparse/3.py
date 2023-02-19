#!python3

class useprop:
    _a: str

    @property
    def a(self):
        return self._a

    @a.setter
    def aset(self, v):
        self._a = v

    def __init__(self, **kwargs):
        cmds = {
            "a": self.aset
        }
        for k, v in kwargs.items():
            if k in cmds:
                cmds[k](v)

a=useprop(a=1,b=2)
print(a.__dict__)
