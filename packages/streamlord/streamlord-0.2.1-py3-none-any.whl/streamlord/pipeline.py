import collections.abc
import typing

from .definitions import contracts

T = typing.TypeVar('T')


class Pipe(typing.Generic[T]):
    def __init__(self, stream: contracts.Stream[T]):
        self._stream = stream
        self._mappers = []
        self._filters = []

    def map(self, *func: collections.abc.Callable[[T], typing.Any]) -> typing.Self:
        self._mappers.extend(list(func))
        return self

    def filter(self, *func: collections.abc.Callable[[T], bool]) -> typing.Self:
        self._filters.extend(list(func))
        return self

    def collect(self, func: collections.abc.Callable[[contracts.Stream[T]], typing.Any] = None) -> typing.Any:
        stream = self._stream
        for filter_func in self._filters:
            stream = filter(filter_func, stream)

        for map_func in self._mappers:
            stream = map(map_func, stream)

        return func(stream) if func else stream
