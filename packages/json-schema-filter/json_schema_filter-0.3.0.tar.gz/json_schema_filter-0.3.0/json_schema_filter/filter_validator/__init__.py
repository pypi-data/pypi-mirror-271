# flake8: noqa: F401

import os
import sys

from .registry import FilterValidatorRegistry

dir_path = os.path.dirname(os.path.abspath(__file__))
files_in_dir = [
    f[:-3]
    for f in os.listdir(dir_path)
    if f.endswith(".py") and f.endswith("_validator.py")
]
for f in files_in_dir:
    mod = __import__(".".join([__name__, f]), fromlist=[f])
    to_import = [
        getattr(mod, x) for x in dir(mod) if hasattr(getattr(mod, x), "__wrapped__")
    ]

    for i in to_import:
        try:
            setattr(sys.modules[__name__], i.__name__, i)
        except AttributeError:
            pass
