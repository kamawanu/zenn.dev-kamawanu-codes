from v0 import Validator


class User:
    _validator_ = Validator.validate_user


class Article:
    _validator_ = Validator.validate_article


def validate_obj(obj):
    return obj._validator_()


if __name__ == "__main__":
    user = User()
    validate_obj(user)

    article = Article()
    validate_obj(article)
