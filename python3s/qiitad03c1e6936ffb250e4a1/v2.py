from typing import Callable, Type, T, Dict
from v0 import Validator


class validateuserregistory:
    map_: Dict[Type,Callable]

    def __init__(self) -> None:
        self.map_ = {}

    def __call__(self, cls:Type[T]) -> Type[T]:
        func = getattr(Validator, f"validate_{cls.__name__.lower()}")
        self.map_.update({cls: func})
        return cls

    def invoker(self, obj):
        return self.map_[type(obj)](obj)


maybe_uses_validator = validateuserregistory()


@maybe_uses_validator
class User:
    pass


@maybe_uses_validator
class Article:
    pass


validate_obj = maybe_uses_validator.invoker

user = User()
validate_obj(user)

article = Article()
validate_obj(article)
