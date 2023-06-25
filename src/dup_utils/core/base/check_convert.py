import ast
from typing import (
    Any,
    Optional,
    Tuple,
    Union,
)

StringTrue: Tuple[str, ...] = (
    "yes",
    "true",
    "t",
    "1",
    "y",
    "1.0",
)
StringFalse: Tuple[str, ...] = ("no", "false", "f", "0", "n", "0.0")


def is_int(value: Any) -> bool:
    """Check value that able to be integer of float

    .. docs::
        https://stackoverflow.com/questions/1265665/how-can-i-check-if-a-string-represents-an-int-without-using-try-except

    .. usage::
        >>> is_int('')
        False
        >>> is_int('0.0')
        False
        >>> is_int('-3')
        True
        >>> is_int('-123.4')
        False
        >>> is_int('543')
        True
        >>> is_int('0')
        True
        >>> is_int('-')
        False
    """
    if isinstance(value, int):
        return True
    _value = str(value)
    if not value:
        return False
    # ``str.isdigit()`` or ``str.isdecimal()`` or ``str.isnumeric()``
    return (
        _value[1:].isdecimal()
        if _value[0] in {"-", "+"}
        else _value.isdecimal()
    )


def can_int(value: Any) -> bool:
    """
    .. usage:
        >>> can_int('0.0')
        True
        >>> can_int('-1.0')
        True
    """
    try:
        return float(str(value)).is_integer()
    except (TypeError, ValueError):
        return False


def str2bool(
    value: Optional[str] = None,
    force_raise: bool = True,
) -> bool:
    """
    :usage:
        >>> str2bool('yes')
        True
        >>> str2bool('false')
        False
    """
    value = value or ""
    if not value:
        return False
    elif value.lower() in StringTrue:
        return True
    elif value.lower() in StringFalse:
        return False
    if force_raise:
        raise ValueError(f"value {value!r} does not convert to boolean type")
    return False


def str2list(
    value: Optional[str] = None,
    force_raise: bool = True,
) -> list:
    """
    :usage:
        >>> str2list('["a", "b", "c"]')
        ['a', 'b', 'c']
        >>> str2list('["d""]', force_raise=False)
        ['["d""]']
        >>> str2list('["d""]')
        Traceback (most recent call last):
        ...
        ValueError: can not convert string value '["d""]' to list object
    """
    if value is None or value == "":
        return []
    if value.startswith("[") and value.endswith("]"):
        try:
            return ast.literal_eval(value)
        except SyntaxError as err:
            if not force_raise:
                return [value]
            raise ValueError(
                f"can not convert string value {value!r} to list object"
            ) from err
    return [value]


def str2dict(value: Optional[str] = None, force_raise: bool = True) -> dict:
    """
    :usage:
        >>> str2dict('{"a": 1, "b": 2, "c": 3}')
        {'a': 1, 'b': 2, 'c': 3}
        >>> str2dict('{"d""}', force_raise=False)
        {1: '{"d""}'}
        >>> str2dict('{"d""}')
        Traceback (most recent call last):
        ...
        ValueError: can not convert string value '{"d""}' to dict object
    """
    if value is None or value == "":
        return {}
    if value.startswith("{") and value.endswith("}"):
        try:
            return ast.literal_eval(value)
        except SyntaxError as err:
            if not force_raise:
                return {1: value}
            raise ValueError(
                f"can not convert string value {value!r} to dict object"
            ) from err
    return {1: value}


def str2int_float(
    value: Optional[str] = None,
    force_raise: bool = False,
) -> Union[int, float]:
    """
    :usage:
        >>> str2int_float('+3')
        3
        >>> str2int_float('-5.00')
        -5.0
        >>> str2int_float('-3.01')
        -3.01
        >>> str2int_float('[1]')
        0
        >>> str2int_float('x0', force_raise=True)
        Traceback (most recent call last):
        ...
        ValueError: can not convert string value 'x0' to int or float
    """
    if value is None or value == "":
        return 0
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError as err:
            if not force_raise:
                return 0
            raise ValueError(
                f"can not convert string value {value!r} to int or float"
            ) from err


def must_list(value: Optional[Union[str, list]] = None) -> list:
    if value:
        return str2list(value) if isinstance(value, str) else value
    return []


def must_bool(
    value: Optional[Union[str, int, bool]] = None, force_raise: bool = False
) -> bool:
    """
    .. usage::
        >>> must_bool('1')
        True
        >>> must_bool(0)
        False
        >>> must_bool("[1, 2, 'foo']")
        False
    """
    if value:
        return (
            value
            if isinstance(value, bool)
            else str2bool(str(value), force_raise=force_raise)
        )
    return False


def str2any(value: str) -> Any:
    """Convert string value to real type.
    :usage:
        >>> str2any('1245')
        1245
        >>> str2any('"string"')
        'string'
        >>> str2any('[1, 2, 3]')
        [1, 2, 3]
        >>> str2any('{"key": "value"}')
        {'key': 'value'}
        >>> str2any('1245.123')
        '1245.123'
        >>> str2any('True')
        True
    """
    if value.startswith(('"', "'")) and value.endswith(('"', "'")):
        return value.strip("\"'")
    elif value.isdecimal():
        return str2int_float(value)
    elif value.startswith("[") and value.endswith("]"):
        return str2list(value)
    elif value.startswith("{") and value.endswith("}"):
        return str2dict(value)
    elif value in {
        "True",
        "False",
    }:
        return str2bool(value)
    return value


def revert_args(*args, **kwargs) -> Tuple[tuple, dict]:
    """Return arguments and key-word arguments.
    .. usage::
        >>> revert_args('value', 1, name='demo', _dict={'k1': 'v1', 'k2': 'v2'})
        (('value', 1), {'name': 'demo', '_dict': {'k1': 'v1', 'k2': 'v2'}})
    """
    return args, kwargs


def str2args(value: Optional[str]) -> Tuple[tuple, dict]:
    """Convert arguments string to args and kwargs
    .. usage::
        >>> str2args("'value', 1, name='demo'")
        (('value', 1), {'name': 'demo'})

        >>> str2args("'value', 1, '[1, 3, \\"foo\\"]'")
        (('value', 1, '[1, 3, "foo"]'), {})

    """
    return eval(f"revert_args({value})")
