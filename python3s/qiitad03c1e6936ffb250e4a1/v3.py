from v0 import Validator


def mixin_validator_of(func:callable) -> type:
    class _:
        _validator_ = func
    return _


class User(mixin_validator_of(Validator.validate_user)):
    pass


class Article(mixin_validator_of(Validator.validate_article)):
    pass

def validate_obj(obj):
    return obj._validator_()

user = User()
validate_obj(user)

article = Article()
validate_obj(article)
