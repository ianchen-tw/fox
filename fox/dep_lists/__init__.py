import importlib
from typing import List

from fox.schemas import Department, Semester

# cached_sems = [(108, "1"), (109, "1")]

# only cache for 3 year
cached_sems = [
    Semester(year=110, term="1"),
    #
    Semester(year=109, term="X"),
    Semester(year=109, term="2"),
    Semester(year=109, term="1"),
    #
    Semester(year=108, term="X"),
    Semester(year=108, term="2"),
    Semester(year=108, term="1"),
]


def cache_get_deps(sem: Semester):
    data: List[Department]
    # try:
    module = importlib.import_module(f"fox.dep_lists.data_{sem.year}_{sem.term}")
    data = module.data
    return data
    # except Exception as e:
    #     return None


__all__ = ["cached_sems", "cache_get_deps"]
