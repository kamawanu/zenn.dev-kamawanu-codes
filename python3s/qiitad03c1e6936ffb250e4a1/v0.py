class Validator:
    @staticmethod
    def validate_user(user):
        print(f"call validate_user {user}")

    @staticmethod
    def validate_article(article):
        print(f"call validate_article {article}")


def validate_obj(obj):
    validate_type = obj.__class__.__name__.lower()
    f = getattr(Validator, "validate_"+validate_type)
    return f(obj)


class User:
    pass


class Article:
    pass


if __name__ == "__main__":
    user = User()
    validate_obj(user)

    article = Article()
    validate_obj(article)
