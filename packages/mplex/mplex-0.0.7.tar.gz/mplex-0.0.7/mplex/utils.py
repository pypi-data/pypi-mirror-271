from fractions import Fraction
from numbers import Real
from typing import Any

import numpy as np

_to_inch = {
    "pt": Fraction(1 / 72),
    "inch": Fraction(1),
    "in": Fraction(1),
    "cm": Fraction(50, 127),
    "mm": Fraction(5, 127),
}


def convert_unit(x, fro: str, to: str) -> Any:
    if isinstance(x, Real):
        return float(_to_inch[fro] / _to_inch[to] * x)
    else:
        return (_to_inch[fro] / _to_inch[to] * np.asarray(x)).astype(float)


def is_array(a):
    if hasattr(a, "__len__") and not isinstance(a, str):
        return True

    return False


def to_array(a, n: int):
    if is_array(a):
        return np.asarray(a)

    return np.array([a] * n)


def safe_unpack(a, *, default1=None, default2=None):
    if isinstance(a, (str, dict)):
        a = (a, a)
    try:
        a1, a2 = a
    except (TypeError, ValueError):
        if default1 is None:
            if default2 is None:
                a1 = a2 = a
            else:
                a1, a2 = a, default2
        else:
            if default2 is None:
                a1, a2 = default1, a
            else:
                a1, a2 = default1, default2

    return a1, a2


def safe_len(a):
    try:
        return len(a)
    except TypeError:
        return 1
