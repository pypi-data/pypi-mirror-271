import collections.abc
import typing


class Dig:
    def __init__(
        self,
        path: str
    ):
        self._chain = path.split('.')

    def __call__(
        self,
        data: collections.abc.MutableMapping
    ) -> collections.abc.Iterable[typing.Any]:
        return self._search(data, 0)

    def _search(
        self,
        item: collections.abc.MutableMapping,
        index: int
    ):
        if index < len(self._chain) - 1:
            item = item.get(self._chain[index])
            if isinstance(item, collections.abc.MutableMapping):
                return self._search(item, index + 1)
            else:
                return None
        else:
            return item.get(self._chain[index])
