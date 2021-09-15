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
