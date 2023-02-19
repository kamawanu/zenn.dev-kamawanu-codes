#!python3

class usesetter:
    a:str
    b:str
    c:str
    def __init__(self,**kwargs):
        if "a" in kwargs:
            self.a = kwargs["a"]
        if "b" in kwargs:
            self.b = kwargs["b"]
        if "c" in kwargs:
            self.c = kwargs["c"]

a=usesetter(a=1,b=2)
print(a.__dict__)
