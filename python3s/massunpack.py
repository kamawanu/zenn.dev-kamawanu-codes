
def func1(*, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False, match_args=True, kw_only=False, slots=False, weakref_slot=False):
    ...

func1( init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False, match_args=True, kw_only=False, slots=False, weakref_slot=False)

import dataclasses

@dataclasses.dataclass(kw_only=True)
class func1inject:
    init:bool
    repr:bool
    eq:bool
    order:bool
    unsafe_hash:bool
    frozen:bool
    match_args:bool
    kw_only:bool
    slots:bool
    weakref_slot:bool

def func1(**vargs):
    inject = func1inject(**vargs)
    print(inject)
    ...

func1( init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False, match_args=True, kw_only=False, slots=False, weakref_slot=False)

def func1(*,inject=None,**vargs):
    if inject is None:
        inject = func1inject(**vargs)
    ...
    print(inject)

func1( init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False, match_args=True, kw_only=False, slots=False, weakref_slot=False)

class class1:
    config:func1inject
    def __init__(self,**vargs):
        self.config = func1inject(**vargs)
