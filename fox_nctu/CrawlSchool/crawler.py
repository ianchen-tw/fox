from typing import List
from .objects import Term, Semester, Department, Course
from .dep_manager import DepManager


class Crawler:
    @staticmethod
    def get_deps(sem: Semester, reuse: bool = True) -> List[Department]:
        dep_manager = DepManager(sem, reuse)
        deps = dep_manager.get_deps()
        return deps

    @staticmethod
    def get_courses(sem: Semester, dep: Department, reuse: bool = True) -> List[Course]:
        # TODO : get_courses
        pass
