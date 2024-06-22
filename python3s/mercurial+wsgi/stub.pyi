from typing import Callable, Optional, Union


START_RESPONSE = Callable[[int, dict[str, str]], None]


def wsgiapplication(app_maker: callable) -> Callable[[dict], START_RESPONSE]:
    ...


class BasicAuth:
    def authenticate(self, env: dict[str, str]) -> bool:
        ...


def parse(auth: str) -> Optional[tuple[str, str]]:
    ...


class ui:
    ...


class hgwebdir:
    def __init__(conf: Union[dict, tuple, bytes], baseui: ui):
        ...
