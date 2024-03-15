import dataclasses
from typing import List, Dict, Any

@dataclasses.dataclass
class classdeco:
    func:callable = None
    _: dataclasses.KW_ONLY
    args:str = None
    def __call__(self, *args, **kwargs):
        if self.func is None and callable(args[0]):
            self.func = args[0]
            return self
        else:
            self._preprocess(args,kwargs)
            return self.func(*args,**kwargs)
    def _preprocess(self,args:List[Any],kwargs:dict[Any,Any]):
        ...

@classdeco
def func1():
    ...

@classdeco(args=1)
def func2():
    ...

func1()
func2()
print(func1)
print(func2)
