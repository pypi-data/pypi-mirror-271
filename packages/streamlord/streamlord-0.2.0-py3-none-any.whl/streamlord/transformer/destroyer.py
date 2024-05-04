import collections


class RemoveKey:
    def __init__(self, path: str):
        self._chain = path.split('.')

    def __call__(
        self,
        data: collections.abc.MutableMapping
    ) -> collections.abc.MutableMapping:
        block = self._search_block(data, 0)
        if isinstance(block, collections.abc.MutableMapping) and self._chain[-1] in block:
            del block[self._chain[-1]]
        return data

    def _search_block(
        self,
        data: collections.abc.MutableMapping,
        index: int
    ):
        if index < len(self._chain) - 1:
            data = data.get(self._chain[index])
            if isinstance(data, collections.abc.MutableMapping):
                return self._search_block(data, index + 1)
            else:
                return None
        else:
            return data
