import typing as t


def cache_read(
    img,
    read_func: t.Callable,
    is_exist_func: t.Callable,
    cache_func: t.Callable,
):
    """
    read_func: read img function
    judge_func: return True if the img is already cached
    cache_func: give img return the recorded picture
    """

    if is_exist_func(img):
        return cache_func(img)
    return read_func(img)
