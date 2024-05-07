import typing as t


def cache_read(
    img,
    read_func: t.Callable,
    read_cache: t.Callable,
    write_cache: t.Callable,
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
