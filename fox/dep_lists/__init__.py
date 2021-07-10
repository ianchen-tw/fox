import importlib
from typing import List

from fox.schemas import Department, Semester, Term


# cached_sems = [(108, "1"), (109, "1")]

# only cache for 3 year
cached_sems = [
    Semester.from_digit(year=110, term_str="1"),
    #
    Semester.from_digit(year=109, term_str="X"),
    Semester.from_digit(year=109, term_str="2"),
    Semester.from_digit(year=109, term_str="1"),
    #
    Semester.from_digit(year=108, term_str="X"),
    Semester.from_digit(year=108, term_str="2"),
    Semester.from_digit(year=108, term_str="1"),
]


def cache_get_deps(sem: Semester):
    data: List[Department]
    # try:
    module = importlib.import_module(f"fox.dep_lists.data_{sem.year}_{sem.term.value}")
    data = module.data
    return data
    # except Exception as e:
    #     return None


__all__ = ["cached_sems", "cache_get_deps"]
