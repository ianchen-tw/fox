from pathlib import Path

from fox.cache import FoxCache


def test_cache_dogfooding(tmp_path: Path):
    target = tmp_path / "test.json"
    cache = FoxCache(target_path=target)

    cache.save([1, 5, 10])
    obj = cache.load()
    assert obj == [1, 5, 10]


def test_cache_will_create_path(tmp_path: Path):
    parent_path = tmp_path / "parent_folder"
    target = parent_path / "test.json"
    cache = FoxCache(target_path=target)
    cache.save([1, 5, 10])
    assert parent_path.exists() and parent_path.is_dir()


def test_cache_encoder(tmp_path):
    target = tmp_path / "test.json"
    cache = FoxCache(target_path=target, encode_func=lambda x: [a + 1 for a in x])
    cache.save([1, 5, 10])
    obj = cache.load()
    assert obj == [2, 6, 11]


def test_cache_decoder(tmp_path):
    target = tmp_path / "test.json"
    cache = FoxCache(target_path=target, decode_func=lambda x: [a - 1 for a in x])
    cache.save([1, 5, 10])
    obj = cache.load()
    assert obj == [0, 4, 9]


def test_cache_corrupt(tmp_path):
    target = tmp_path / "test.json"
    with open(target, "w") as fp:
        fp.write('{"a":a')
    cache = FoxCache(target_path=target)
    assert cache.load() is None


def test_cache_no_file(tmp_path):
    target = tmp_path / "something_not_existed.json"
    cache = FoxCache(target_path=target)
    assert cache.load() is None
