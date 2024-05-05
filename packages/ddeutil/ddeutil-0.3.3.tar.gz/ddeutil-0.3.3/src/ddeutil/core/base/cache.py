from __future__ import annotations

from functools import wraps
from typing import Any


class memoize:
    """Return a cachable function that keep all argruments and pass to string
    type for keeping it in the caching key.

    :usage:
        >>> @memoize
        ... def fib(n):
        ...     if n in (0, 1):
        ...         return 1
        ...     else:
        ...         return fib(n-1) + fib(n-2)
        >>> for i in range(0, 5):
        ...     fib(i)
        1
        1
        2
        3
        5
    """

    def __init__(self, function):
        self.cache: dict[str, Any] = {}
        self.function = function

    def __call__(self, *args, **kwargs) -> Any:
        key: str = str(args) + str(kwargs)
        if key in self.cache:
            return self.cache[key]

        value: Any = self.function(*args, **kwargs)
        self.cache[key] = value
        return value


def memoized_property(func_get):
    """Return a property attribute for new-style classes that only calls its
    getter on the first access. The result is stored and on subsequent
    accesses is returned, preventing the need to call the getter anymore.

    :usage:
        >>> class C(object):
        ...     load_name_count = 0
        ...     @memoized_property
        ...     def name(self) -> str:
        ...         "name's docstring"
        ...         self.load_name_count += 1
        ...         return "the name"
        >>> c = C()
        >>> c.load_name_count
        0
        >>> c.name
        'the name'
        >>> c.load_name_count
        1
        >>> c.name
        'the name'
        >>> c.load_name_count
        1
    """
    attr_name = f"_{func_get.__name__}"

    @wraps(func_get)
    def func_get_memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func_get(self))
        return getattr(self, attr_name)

    return property(func_get_memoized)


def clear_cache(attrs: tuple):
    """Clear or delete attribute value of the class that implement cache.
    :usage:
        >>> class C(object):
        ...     load_name_count = 0
        ...     @memoized_property
        ...     def name(self) -> str:
        ...         "name's docstring"
        ...         self.load_name_count += 1
        ...         return "the name"
        ...     @clear_cache(attrs=('_name', ))
        ...     def reset(self) -> str:
        ...         return "reset cache"
        >>> c = C()
        >>> c.load_name_count
        0
        >>> c.name
        'the name'
        >>> c.load_name_count
        1
        >>> c.reset()
        'reset cache'
        >>> c.name
        'the name'
        >>> c.load_name_count
        2
        >>> c.name
        'the name'
        >>> c.load_name_count
        2
    """

    def clear_cache_internal(func_get):
        @wraps(func_get)
        def func_clear_cache(self, *args, **kwargs):
            for attr in attrs:
                if hasattr(self, attr):
                    delattr(self, attr)
            return func_get(self, *args, **kwargs)

        return func_clear_cache

    return clear_cache_internal
