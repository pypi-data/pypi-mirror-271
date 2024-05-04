import collections.abc
import typing

T = typing.TypeVar('T')


class Stream(typing.Generic[T]):
    def __iter__(self) -> collections.abc.Iterable[T]: ...
