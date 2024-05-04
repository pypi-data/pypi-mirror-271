import collections.abc


def first(
    stream: collections.abc.Iterable[collections.abc.MutableMapping]
):
    return next(iter(stream), None)
