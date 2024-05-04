import collections.abc


class Stamp:
    def __init__(self, parent_key: str, *nested_keys: str | tuple[str, str]):
        super().__init__()
        self._parent_chain = parent_key.split('.')
        self._nested_keys = [k if isinstance(k, tuple) else (k, k) for k in nested_keys]

    def __call__(self, data: collections.abc.MutableMapping):
        self._process(data)
        return data

    def _process(
        self,
        data: collections.abc.MutableMapping,
        index: int = 0
    ):
        if index < len(self._parent_chain) - 1:
            data = data.get(self._parent_chain[index])
            if isinstance(data, collections.abc.MutableMapping):
                self._process(data, index + 1)
            elif isinstance(data, collections.abc.Sequence):
                for item in data:
                    self._process(item, index + 1)
        else:
            data[self._parent_chain[-1]] = {
                                               keys[1]: data[keys[0]]
                                               for keys in self._nested_keys
                                               if data[keys[0]] is not None
                                           } or None
            for keys in self._nested_keys:
                if keys[0] in data:
                    del data[keys[0]]
