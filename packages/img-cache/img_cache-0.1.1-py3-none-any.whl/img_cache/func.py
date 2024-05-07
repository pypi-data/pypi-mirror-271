import typing as t
from . import types as T


def cache_read(
    img,
    read_func: T.ReadFunc,
    read_cache: T.ReadCache,
    write_cache: T.WriteCache,
):
    """
    read_func: read img function
    cache_func: give img return the recorded picture
    read_cache: read cache function
    write_cache: write cache function
    """

    res = read_cache(img)
    if res:
        return res

    res = read_func(img)
    return write_cache(img, res)
