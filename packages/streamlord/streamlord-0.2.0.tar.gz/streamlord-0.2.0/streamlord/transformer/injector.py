import collections.abc


class Inject:
    def __init__(
        self,
        reference: collections.abc.Mapping,
        search_path: str,
        injection_path: str,
        replace: bool = False
    ):
        self._reference = reference
        self._search_chain = search_path.split('.')
        self._injection_chain = injection_path.split('.')
        self._replace = replace

    def __call__(
        self,
        data: collections.abc.MutableMapping
    ) -> collections.abc.MutableMapping:
        self._process(data, 0)
        return data

    def _process(
        self,
        data: collections.abc.MutableMapping,
        index: int
    ):
        if index < len(self._search_chain) - 1:
            data = data.get(self._search_chain[index])
            if isinstance(data, collections.abc.MutableMapping):
                self._process(data, index + 1)
            elif isinstance(data, collections.abc.Sequence):
                for item in data:
                    self._process(item, index + 1)
        else:
            key_value = data.get(self._search_chain[index])
            data_value = self._reference.get(key_value)
            data[self._injection_chain[-1]] = data_value
            if self._replace:
                del data[self._search_chain[-1]]
