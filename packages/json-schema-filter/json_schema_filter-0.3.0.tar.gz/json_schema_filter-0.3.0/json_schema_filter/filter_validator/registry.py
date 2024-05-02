from functools import wraps
from typing import Callable, Dict


class FilterValidatorRegistry:
    registered_validators: Dict = {}

    @classmethod
    def register(cls, fn: Callable):
        cls.registered_validators[fn.__name__] = fn

        @wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)

        return wrapper
