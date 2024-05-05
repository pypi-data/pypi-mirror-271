import re
from collections.abc import Iterator
from typing import AnyStr


def split_str(strings, sep: str = r"\s+") -> Iterator[str]:
    """
    warning: does not yet work if sep is a lookahead like `(?=b)`
    usage:
        >>> list(split_str('A,b,c.', sep=','))
        ['A', 'b', 'c.']
        >>> list(split_str(',,A,b,c.,', sep=','))
        ['', '', 'A', 'b', 'c.', '']
        >>> list(split_str('.......A...b...c....', '...'))
        ['', '', '.A', 'b', 'c', '.']
        >>> list(split_str('   A  b  c. '))
        ['', 'A', 'b', 'c.', '']
    """
    if not sep:
        return iter(strings)
    sep = sep.replace(".", "\\.")
    # alternatively, more verbosely:
    regex = f"(?:^|{sep})((?:(?!{sep}).)*)"
    for match in re.finditer(regex, strings):
        yield match.group(1)


def isplit(source: AnyStr, sep=None, regex=False):
    """Generator of ``str.split()`` method.

    :param source: source string (unicode or bytes)
    :param sep: separator to split on.
    :param regex: if True, will treat sep as regular expression.

    :returns:
        generator yielding elements of string.

    Examples:
        >>> list(isplit("abcb", "b"))
        ['a', 'c', '']
        >>> next(isplit("foo bar"))
        'foo'
    """
    if sep is None:
        # mimic default python behavior
        source = source.strip()
        sep = "\\s+"
        if isinstance(source, bytes):
            sep = sep.encode("ascii")
        regex = True
    start = 0
    if regex:
        # version using re.finditer()
        if not hasattr(sep, "finditer"):
            sep = re.compile(sep)
        for m in sep.finditer(source):
            idx = m.start()
            assert idx >= start
            yield source[start:idx]
            start = m.end()
        yield source[start:]
    else:
        # version using str.find(), less overhead than re.finditer()
        sep_size = len(sep)
        while True:
            idx = source.find(sep, start)
            if idx == -1:
                yield source[start:]
                return
            yield source[start:idx]
            start = idx + sep_size


def split(
    source: str,
    sep: str = None,
    *,
    maxsplit: int = -1,
    mustsplit: bool = True,
) -> list[str]:
    """
    Examples:
        >>> split('asd|fasd', '|', maxsplit=2)
        ['asd', 'fasd', None]
        >>> split('data', '.', maxsplit=1)
        ['data', None]
    """
    if maxsplit == -1 or not mustsplit:
        return source.split(sep, maxsplit)
    _old: list = source.split(sep, maxsplit)
    _result: list = [None] * ((maxsplit + 1) - len(_old))
    _old.extend(_result)
    return _old


def rsplit(
    source: str,
    sep: str = None,
    *,
    maxsplit: int = -1,
    mustsplit: bool = True,
) -> list[str]:
    """
    Examples:
        >>> rsplit('asd|foo', '|', maxsplit=2)
        [None, 'asd', 'foo']
        >>> rsplit('foo bar', maxsplit=1)
        ['foo', 'bar']
        >>> rsplit('foo bar', maxsplit=2, mustsplit=False)
        ['foo', 'bar']
    """
    if maxsplit == -1 or not mustsplit:
        return source.rsplit(sep, maxsplit=maxsplit)
    _old: list = source.rsplit(sep, maxsplit)
    _result: list = [None] * ((maxsplit + 1) - len(_old))
    _result.extend(_old)
    return _result
