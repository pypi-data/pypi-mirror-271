import pint
from typing import Number

UREG = pint.UnitRegistry()


def add_dollar(a, b):
    try:
        return a + b
    except:
        return None


def add_portion(a, b):
    """Portion addition

    Returns
    -------
    pint.Quantity
        Addition is only defined when both inputs are pint.Quantity.
        For str and Number, the unit is unrecognized and thus addition
        cannot be performed.
    """
    if isinstance(a, pint.Quantity) and isinstance(b, pint.Quantity):
        return a + b
    return None


def parse_portion(x):
    """Parse portion

    Returns
    -------
    Number | str | pint.Quantity
        Depending on the input and whether the parsing succeeded, the 
        returned value could either be `Number`, `str`, or `pint.Quantity`.

        When input x is `str`, the returned value is either 
        `pint.Quantity` or `str`, depending on whether pint recognizes the
        unit in the passed in value.

        If the input x is `pint.Quantity` or `Number`, no parsing is done 
        and the input is returned as output.
    """
    if isinstance(x, pint.Quantity) or isinstance(x, Number):
        return x
    if isinstance(x, str):
        try:
            return UREG(x)
        except:
            return x
    raise Exception("Unsupported input type. Only (str|Number|pint.Quantity) are allowed.")
