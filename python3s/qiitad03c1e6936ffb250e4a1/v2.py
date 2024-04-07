from typing import Any
from v0 import Validator


class validateuserregistory:
    map_: dict

    def __init__(self) -> None:
        self.map_ = {}

    def __call__(self, cls) -> Any:
        func = getattr(Validator, f"validate_{cls.__name__.lower()}")
        self.map_.update({cls: func})
        return cls

    def invoker(self, obj):
        return self.map_[type(obj)](obj)


can_validate = validateuserregistory()


@can_validate
class User:
    pass


@can_validate
class Article:
    pass


validate_obj = can_validate.invoker

user = User()
validate_obj(user)

article = Article()
validate_obj(article)
