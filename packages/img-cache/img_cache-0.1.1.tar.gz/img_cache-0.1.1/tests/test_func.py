import typing as t
from img_cache.func import cache_read
from img_cache.sample import memory_cache_func


# use string to represent img.
def read_meter(img: t.Any):
    read_count = {}
    read_count[img] = read_count.get(img, 0) + 1
    return "res" + img


def fake_img(name="test"):
    return name + "1123"


def test_two_dict():
    def cache_dict():
        return {}

    cache_1 = cache_dict()
    cache_2 = cache_dict()
    assert cache_1 is not cache_2, "two cache should be different"


def test_cache_read():
    # cache result should be the same as the original result
    for name in ["test", "test1"]:
        res1 = read_meter(fake_img(name))
        r, w = memory_cache_func(lambda x: x)
        res2 = cache_read(
            fake_img(name),
            read_func=read_meter,
            read_cache=r,
            write_cache=w,
        )
        assert res1 == res2, "cache result should be the same as the original result"


def test_cache_func():
    r, w = memory_cache_func(lambda x: x)
    w("test2", "v_test2")
    assert r("test2")
    assert r("test1") is None, "cache should be empty"


def test_cache_read2():
    # diffrent result should return different
    r, w = memory_cache_func(lambda x: x)
    img = fake_img("test2")
    res1 = read_meter(img)
    assert r(img) is None, "cache should be empty"

    img = fake_img("test1")
    res2 = cache_read(
        img=img,
        read_func=read_meter,
        read_cache=r,
        write_cache=w,
    )
    assert res1 != res2, "cache result should be different from the original result"
    assert r(img), "cache should not be empty"
