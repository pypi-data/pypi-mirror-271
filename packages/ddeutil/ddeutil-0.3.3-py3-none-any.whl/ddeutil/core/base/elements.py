from __future__ import annotations

from collections.abc import Collection
from numbers import Number
from typing import (
    Any,
    Optional,
)

try:
    from .splitter import split
except ImportError:
    from splitter import split


ZERO_DEPTH_BASES = (
    str,
    bytes,
    Number,
    range,
    bytearray,
)


def only_one(
    check: list[str],
    value: list[str],
    default: bool = True,
) -> Optional[str]:
    """Get only one element from check list that exists in match list.

    Examples:
        >>> only_one(['a', 'b'], ['a', 'b', 'c'])
        'a'
        >>> only_one(['a', 'b'], ['c', 'e', 'f'])
        'c'
        >>> only_one(['a', 'b'], ['c', 'e', 'f'], default=False)

    """
    if len(exist := set(check).intersection(set(value))) == 1:
        return list(exist)[0]
    return next(
        (_ for _ in value if _ in check),
        (value[0] if default else None),
    )


def hasdot(search: str, content: dict[Any, Any]) -> bool:
    """Return True value if dot searching exists in content data.

    Examples:
        >>> hasdot('data.value', {'data': {'value': 2}})
        True
        >>> hasdot('data.value.key', {'data': {'value': 2}})
        False
        >>> hasdot('item.value.key', {'data': {'value': 2}})
        False
    """
    _search, _else = split(search, ".", maxsplit=1)
    if _search in content and isinstance(content, dict):
        if not _else:
            return True
        elif isinstance((result := content[_search]), dict):
            return hasdot(_else, result)
    return False


def getdot(
    search: str,
    content: dict[Any, Any],
    *args,
    **kwargs,
) -> Any:
    """Return the value if dot searching exists in content data.

    Examples:
        >>> getdot('data.value', {'data': {'value': 1}})
        1
        >>> getdot('data', {'data': 'test'})
        'test'
        >>> getdot('data.value', {'data': 'test'})
        Traceback (most recent call last):
        ...
        ValueError: 'value' does not exists in test
        >>> getdot('data.value', {'data': {'key': 1}}, None)

        >>> getdot(
        ...     'data.value.getter',
        ...     {'data': {'value': {'getter': 'success', 'put': 'fail'}}},
        ... )
        'success'
        >>> getdot('foo.bar', {"foo": {"baz": 1}}, ignore=True)

        >>> getdot('foo.bar', {"foo": {"baz": 1}}, 2, 3)
        2
        >>> getdot('foo.bar', {"foo": {"baz": 1}}, 2, 3, ignore=True)
        2
    """
    _ignore: bool = kwargs.get("ignore", False)
    _search, _else = split(search, ".", maxsplit=1)
    if _search in content and isinstance(content, dict):
        if not _else:
            return content[_search]
        if isinstance((result := content[_search]), dict):
            return getdot(_else, result, *args, **kwargs)
        if _ignore:
            return None
        raise ValueError(f"{_else!r} does not exists in {result}")
    if args:
        return args[0]
    elif _ignore:
        return None
    raise ValueError(f"{_search} does not exists in {content}")


def setdot(search: str, content: dict, value: Any, **kwargs) -> dict:
    """
    Examples:
        >>> setdot('data.value', {'data': {'value': 1}}, 2)
        {'data': {'value': 2}}
        >>> setdot('data.value.key', {'data': {'value': 1}}, 2, ignore=True)
        {'data': {'value': 1}}
    """
    _ignore: bool = kwargs.get("ignore", False)
    _search, _else = split(search, ".", maxsplit=1)
    if _search in content and isinstance(content, dict):
        if not _else:
            content[_search] = value
            return content
        if isinstance((result := content[_search]), dict):
            content[_search] = setdot(_else, result, value, **kwargs)
            return content
        if _ignore:
            return content
        raise ValueError(f"{_else!r} does not exists in {result}")
    if _ignore:
        return content
    raise ValueError(f"{_search} does not exists in {content}")


def filter_dict(
    value: dict[Any, Any],
    included: Optional[Collection] = None,
    excluded: Optional[Collection] = None,
):
    """
    Examples:
        >>> filter_dict({"foo": "bar"}, included={}, excluded={"foo"})
        {}

        >>> filter_dict(
        ...     {"foo": 1, "bar": 2, "baz": 3},
        ...     included=("foo", )
        ... )
        {'foo': 1}

        >>> filter_dict(
        ...     {"foo": 1, "bar": 2, "baz": 3},
        ...     included=("foo", "bar", ),
        ...     excluded=("bar", )
        ... )
        {'foo': 1}
    """
    _exc = excluded or ()
    return dict(
        filter(
            lambda i: i[0]
            in (v for v in (included or value.keys()) if v not in _exc),
            value.items(),
        )
    )
