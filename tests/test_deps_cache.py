from fox.data import cache_get_deps, cached_deps


def test_cache_terms_import():
    for sem in cached_deps:
        data = cache_get_deps(sem)
        assert len(data) > 0
