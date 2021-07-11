from fox.dep_lists import cache_get_deps, cached_sems


def test_cache_terms_import():
    for sem in cached_sems:
        data = cache_get_deps(sem)
        assert len(data) > 0
