from typing import Any, T, Type


def ezconst(srccls: Type[T]) -> T:
    class _(srccls):
        def __setattr__(self, __name: str, __value: Any):
            ...

    return _()


@ezconst
class constantit:
    ONE=1
    TWO=2

if __name__ == "__main__":
    print(constantit)
    print(constantit.ONE) # 1
    constantit.ONE=3
    print(constantit.ONE) # 1
    print(type(constantit).__mro__)
