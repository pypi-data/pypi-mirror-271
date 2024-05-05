from __future__ import annotations

import contextlib
import copy
from functools import wraps
from time import (
    sleep,
    time,
)
from typing import TYPE_CHECKING, Any, Callable, TypeVar

if TYPE_CHECKING:
    import sys

    if sys.version_info >= (3, 10):
        from typing import ParamSpec
    else:
        from typing_extensions import ParamSpec

    P = ParamSpec("P")
    T = TypeVar("T")


def deepcopy(func: Callable[P, T]) -> Callable[P, T]:
    """Deep copy method

    EExamples:
        >>> @deepcopy
        ... def foo(a, b, c=None):
        ...     c = c or {}
        ...     a[1] = 3
        ...     b[2] = 4
        ...     c[3] = 5
        ...     return a, b, c
        >>> aa = {1: 2}
        >>> bb = {2: 3}
        >>> cc = {3: 4}
        >>> foo(aa, bb, cc)
        ({1: 3}, {2: 4}, {3: 5})

        >>> (aa, bb, cc)
        ({1: 2}, {2: 3}, {3: 4})

    """

    def func_get(*args: P.args, **kwargs: P.kwargs) -> T:
        return func(
            *(copy.deepcopy(x) for x in args),
            **{k: copy.deepcopy(v) for k, v in kwargs.items()},
        )

    return func_get


def deepcopy_args(func: Callable[[object, P], T]) -> Callable[[object, P], T]:
    """Deep copy method

    Examples:
        >>> class Foo:
        ...
        ...     @deepcopy_args
        ...     def foo(self, a, b=None):
        ...         b = b or {}
        ...         a[1] = 4
        ...         b[2] = 5
        ...         return a, b
        >>>
        >>> aa = {1: 2}
        >>> bb = {2: 3}
        >>> Foo().foo(aa, bb)
        ({1: 4}, {2: 5})

        >>> (aa, bb)
        ({1: 2}, {2: 3})

    """

    def func_get(self: object, *args: P.args, **kwargs: P.kwargs) -> T:
        return func(
            self,
            *(copy.deepcopy(x) for x in args),
            **{k: copy.deepcopy(v) for k, v in kwargs.items()},
        )

    return func_get


def timer(func: Callable[P, T]) -> Callable[P, T]:
    """
    Examples:
        >>> import time
        >>> @timer
        ... def will_sleep():
        ...     time.sleep(2)
        ...     return
        >>> will_sleep()
        Execution time: 2.003119945526123 seconds
    """

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        start_time = time()
        result = func(*args, **kwargs)
        execution_time = time() - start_time
        print(f"Execution time: {execution_time} seconds")
        return result

    return wrapper


def timing(name: str) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """
    Examples:
        >>> import time
        >>> @timing("Sleep")
        ... def will_sleep():
        ...     time.sleep(2)
        ...     return
        >>> will_sleep()
        Sleep ....................................................... 2.01s
    """

    def timing_internal(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrap(*args: P.args, **kw: P.kwargs) -> T:
            ts = time()
            result = func(*args, **kw)
            padded_name: str = f"{name} ".ljust(60, ".")
            padded_time: str = f" {(time() - ts):0.2f}".rjust(6, ".")
            print(f"{padded_name}{padded_time}s", flush=True)
            return result

        return wrap

    return timing_internal


@contextlib.contextmanager
def timer_perf(title: str):
    """
    Examples:
        >>> import time
        >>> with timer_perf('Sleep'):
        ...     time.sleep(2)
        Sleep ....................................................... 2.00s
    """
    ts = time()
    yield
    te = time()
    padded_name: str = f"{title} ".ljust(60, ".")
    padded_time: str = f" {(te - ts):0.2f}".rjust(6, ".")
    print(f"{padded_name}{padded_time}s", flush=True)


def debug(func: Callable[P, T]) -> Callable[P, T]:
    """
    Examples:
        >>> @debug
        ... def add_numbers(x, y):
        ...     return x + y
        >>> add_numbers(7, y=5, )
        Calling add_numbers with args: (7,) kwargs: {'y': 5}
        add_numbers returned: 12
        12
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs):
        print(f"Calling {func.__name__} with args: {args} kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned: {result}")
        return result

    return wrapper


def validate_input(
    *validations: tuple[Callable[[Any], bool]],
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """
    Examples:
        >>> @validate_input(lambda x: x > 0, lambda y: isinstance(y, str))
        ... def divide_and_print(x: int, message: str):
        ...     print(message)
        ...     return 1 / x
        >>> divide_and_print(5, "Hello!")
        Hello!
        0.2
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            for i, val in enumerate(args):
                if i < len(validations) and not validations[i](val):
                    raise ValueError(f"Invalid argument: {val}")
            for key, val in kwargs.items():
                if key in validations[len(args) :] and not validations[
                    len(args) :
                ][key](val):
                    raise ValueError(f"Invalid argument: {key}={val}")
            return func(*args, **kwargs)

        return wrapper

    return decorator


def retry(
    max_attempts: int,
    delay: int = 1,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Retry decorator with sequencial.
    Examples:
        >>> @retry(max_attempts=3, delay=2)
        ... def fetch_data(url):
        ...     print("Fetching the data ...")
        ...     raise TimeoutError("Server is not responding.")
        >>> fetch_data("https://example.com/data")
        Fetching the data ...
        Attempt 1 failed: Server is not responding.
        Fetching the data ...
        Attempt 2 failed: Server is not responding.
        Fetching the data ...
        Attempt 3 failed: Server is not responding.
        Function `fetch_data` failed after 3 attempts
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            _attempts: int = 0
            while _attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    _attempts += 1
                    print(f"Attempt {_attempts} failed: {e}")
                    sleep(delay)
            print(
                f"Function `{func.__name__}` failed after "
                f"{max_attempts} attempts"
            )

        return wrapper

    return decorator
