from typing import List

from .crawler.course_manager import CourseManager as CourseManager
from .crawler.dep_manager import DepManager as DepManager
from .crawler.target_object.meta_object import Course as Course
from .crawler.target_object.meta_object import Department as Department
from .crawler.target_object.meta_object import Semester as Semester
from .crawler.target_object.meta_object import Term as Term

def main() -> None: ...
def get_deps(sem: Semester, reuse: bool = ...) -> List[Department]: ...
def get_courses(
    sem: Semester, deps: List[Department], reuse: bool = ...
) -> List[Course]: ...
