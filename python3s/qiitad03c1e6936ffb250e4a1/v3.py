from v0 import Validator


def validate_by(func):
    class _:
        _validator_ = func
    return _


class User(validate_by(Validator.validate_user)):
    pass


class Article(validate_by(Validator.validate_article)):
    pass

def validate_obj(obj):
    return obj._validator_()

user = User()
validate_obj(user)

article = Article()
validate_obj(article)
