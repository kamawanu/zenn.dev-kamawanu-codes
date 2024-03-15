import dataclasses
from typing import Any, Callable, Mapping


def ucstr(v):
    return v.upper()

class has_propertysetters:
    def buildsetter(self)->Mapping[str,Callable[[str,],None]]:
        ###print(self.__annotations__)
        kmap = dict()
        for key_, converter_ in self.__annotations__.items():
            @dataclasses.dataclass
            class _:
                parent: has_propertysetters
                key: str
                converter: callable

                def __call__(self, value:Any) -> None:
                    setattr(self.parent, self.key, self.converter(value))

            kmap.update({key_: _(self, key_, converter_)})
            del _
        return kmap
