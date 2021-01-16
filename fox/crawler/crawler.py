from typing import List

from .course_manager import CourseManager
from .dep_manager import DepManager
from .target_object.meta_object import Course, Department, Semester


class Crawler:
    @staticmethod
    def get_deps(sem: Semester, reuse: bool = True) -> List[Department]:
        dep_manager = DepManager(sem, reuse)
        dep_manager.run()
        deps = dep_manager.get_deps()
        return deps

    @staticmethod
    def get_courses(sem: Semester, dep: Department, reuse: bool = True) -> List[Course]:
        course_manager = CourseManager(sem, dep, reuse)
        course_manager.run()
        courses = course_manager.get_courses()
        return courses
