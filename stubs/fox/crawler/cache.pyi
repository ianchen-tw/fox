from pathlib import Path
from typing import Any, List

from .target_object.meta_object import Course as Course
from .target_object.meta_object import Department as Department
from .target_object.meta_object import Semester as Semester
from .types import JSONType as JSONType

class Cache:
    @staticmethod
    def get_path() -> Path: ...
    @staticmethod
    def dep_dump(sem: Semester, deps: Any = ...) -> Any: ...
    @staticmethod
    def dep_load(sem: Semester) -> List[Department]: ...
    @staticmethod
    def course_dump(sem: Semester, dep: Department, courses: Any = ...) -> Any: ...
    @staticmethod
    def course_load(sem: Semester, dep: Department) -> List[Course]: ...
