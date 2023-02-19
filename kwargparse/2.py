#!python3

class usecallale:
    a:str
    b:str
    c:str
    def __init__(self,**kwargs) -> None:
        def seta(x): self.a = x
        cmds = {
            "a": seta
        }
        for k,v in kwargs.items():
            if k in cmds:
                cmds[k](v)

a=usecallale(a=1,c=3)
print(a.__dict__)
