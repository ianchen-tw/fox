from typing import List

from .course_manager import CourseManager as CourseManager
from .dep_manager import DepManager as DepManager
from .target_object.meta_object import Course as Course
from .target_object.meta_object import Department as Department
from .target_object.meta_object import Semester as Semester

class Crawler:
    @staticmethod
    def get_deps(sem: Semester, reuse: bool = ...) -> List[Department]: ...
    @staticmethod
    def get_courses(
        sem: Semester, dep: Department, reuse: bool = ...
    ) -> List[Course]: ...
