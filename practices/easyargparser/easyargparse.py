#!python3
import sys
from typing import List, Dict, Union, Callable, Tuple, Generator, Any


class rawArgType(object):
    becast: callable = None
    short = None
    param = None
    default = None

    def __init__(self, short=None, modifier=None, param=None, default=None):
        self.becast = modifier
        self.short = short
        self.param = param
        self.default = default

    def needopt(self):
        return self.param is not None

    def modify(self, value):
        if self.becast is None:
            return value
        return self.becast(value)


def IntArg(**vargs):
    vargs.update({"param": int, "modifier": int})
    return rawArgType(**vargs)


def BoolArg(**vargs):
    def boolmod(value):
        if value is None:
            return 1
        return value
    vargs.update({"param": int, "modifier": boolmod, "default": False})
    return rawArgType(**vargs)


def StringArg(**vargs):
    vargs.update({"param": str, "modifier": str})
    return rawArgType(**vargs)


class argParseCore(object):
    optmap: Dict[str, Union[str, rawArgType]] = dict()
    singleoptonly = True

    def append(self, k: str, v: rawArgType):
        self.optmap.update({k: v})
        #clr.update({k: v.default})
        if v.short is not None:
            if len(v.short) > 1:
                self.singleoptonly = False
            self.optmap.update({v.short: k})

    def parse(self, argv: List[str]) -> Tuple[List[str], Dict[str, Any]]:
        restarg = []
        result_values = {}

        def _pregrouping(argv: List[str]) -> Generator[List[Union[Tuple[str], str]], None, None]:
            arg_group = []
            in_opt = False
            while len(argv) > 0:
                arg_1, argv = argv[0], argv[1:]
                if arg_1 == "":
                    continue
                if arg_1 == "--":
                    break
                if arg_1[0] == "-":
                    in_opt = True
                    if len(arg_group) > 0:
                        yield arg_group
                    sw_len = _isswitch(arg_1)
                    maybe_switch: List[str] = arg_1[sw_len:].split("=", 1)
                    if sw_len == 1 and self.singleoptonly:
                        ##print(sw_len, self.singleoptonly)
                        maybe_switch[0] = tuple(
                            # charactor slices
                            maybe_switch[0])
                    else:
                        maybe_switch[0] = (maybe_switch[0],)
                    arg_group = maybe_switch
                elif in_opt:
                    arg_group.append(arg_1)
                else:
                    restarg.append(arg_1)
            if len(arg_group) > 0:
                yield arg_group
            restarg.extend(argv)

        for arggrp in _pregrouping(argv):
            pos = 1
            for keyname in arggrp[0]:
                opt = None
                _m: Union[str, rawArgType] = self.optmap[keyname]
                while isinstance(_m, str):
                    keyname = _m
                    _m: rawArgType = self.optmap[keyname]
                # print(_m)
                if _m.needopt() and opt is None and len(arggrp) > pos:
                    opt = arggrp[pos]
                    pos += 1
                opt = _m.modify(opt)
                result_values.update({keyname: opt})
            restarg.extend(arggrp[pos:])

        return restarg, result_values


class ArgParseMeta(type):
    def __new__(basecls, cls_name, cls_bases, cls_instance_dict):
        # if basecls is not (object,):
        ###print('@beforemeta', cls_name, cls_bases, cls_instance_dict)
        parser = argParseCore()
        clr = dict()
        for k, v in cls_instance_dict.items():
            if k[0] != "_" and isinstance(v, rawArgType):
                parser.append(k, v)
                clr.update({k: v.default})
        clr.update({"optmap": parser})
        cls_instance_dict.update(clr)
        ####print('@aftermeta', cls_name, cls_bases, cls_instance_dict)

        return super().__new__(basecls, cls_name, cls_bases, cls_instance_dict)


def _isswitch(key: str) -> int:
    if key[0] == "-" and key[1] != "-":
        return 1
    if key[0] == "-" and key[1] == "-":
        return 2
    return 0


class easyArgParser(object, metaclass=ArgParseMeta):
    _restarg = None
    optmap: argParseCore

    @property
    def restarg(self):
        return self._restarg

    def __init__(self, argv: List[str]):
        self._restarg, _dict = self.optmap.parse(argv)
        self.__dict__.update(_dict)


__all__ = [
    rawArgType.__name__,
    IntArg.__name__,
    BoolArg.__name__,
    StringArg.__name__,
    easyArgParser.__name__,
]
