from typing import List, Optional

from .dep_manager import DepManager
from .objects import Course, Department, Semester


class Crawler:
    @staticmethod
    def get_deps(sem: Semester, reuse: bool = True) -> Optional[List[Department]]:
        dep_manager = DepManager(sem, reuse)
        dep_manager.run()
        deps = dep_manager.get_deps()
        return deps

    @staticmethod
    def get_courses(sem: Semester, dep: Department, reuse: bool = True) -> List[Course]:
        # TODO : get_courses
        pass
