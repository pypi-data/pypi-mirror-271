# sample function for judge_function, cache_function
import typing as t
from . import types as T

# import functools


def md5_serialize():
    # TODO: implement md5_serialize
    pass


def memory_cache_func(serialize: T.Serialize) -> t.Tuple[T.ReadCache, T.WriteCache]:
    """save cache in memory

    serialize: serialize the img to normal string
    """
    return cache_func(lambda: {}, serialize)


def cache_func(get_default_cache: t.Callable, serialize: T.Serialize) -> t.Tuple[T.ReadCache, T.WriteCache]:
    """save cache in provided cache

    get_default_cache: return a default cache
    serialize: serialize the img to normal string
    """
    cache = get_default_cache()

    def read_cache(img):
        s = serialize(img)
        res = cache.get(s, None)
        return res if res else None

    def write_cache(img, v):
        s = serialize(img)
        cache[s] = v
        return cache[s]

    return read_cache, write_cache
