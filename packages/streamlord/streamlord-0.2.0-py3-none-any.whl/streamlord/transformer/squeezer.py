import collections.abc
import typing


class Squeeze:
    def __init__(
        self,
        separator: str = '__',
        collapse_none: bool = True
    ):
        super().__init__()
        self._separator = separator
        self._collapse_none = collapse_none

    def __call__(
        self,
        data: collections.abc.MutableMapping
    ):
        data = self._nestify(data)
        return _collapse_none(data) if self._collapse_none else data

    def _split_rec(self, k, v, out):
        k, *rest = k.split(self._separator, 1)
        if rest:
            self._split_rec(rest[0], v, out.setdefault(k, {}))
        else:
            out[k] = v

    def _nestify(
        self,
        data: typing.Any
    ):
        if isinstance(data, str):
            return data
        elif isinstance(data, bytearray):
            return data
        elif isinstance(data, bytes):
            return data
        elif isinstance(data, collections.abc.Mapping):
            result = {}
            for k, v in data.items():
                self._split_rec(k, self._nestify(v), result)
            return result
        elif isinstance(data, collections.abc.Iterable):
            return [self._nestify(item) for item in data]
        else:
            return data


def _collapse_none(data: collections.abc.Mapping):
    result = {}
    for k, v in data.items():
        if isinstance(v, collections.abc.Mapping):
            v = _collapse_none(v) if any(_ is not None for _ in v.values()) else None
        if isinstance(v, list):
            v = [_collapse_none(_) for _ in v]
        result[k] = v
    return result
