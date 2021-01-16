from typing import Dict

from .target_object.meta_object import College as College
from .target_object.meta_object import CourseCategory as CourseCategory
from .target_object.meta_object import DegreeType as DegreeType
from .target_object.meta_object import Department as Department
from .target_object.meta_object import Semester as Semester
from .types import JSONType as JSONType

def fetch(param: Dict[str, str], form_data: Dict[str, str]) -> JSONType: ...
def get_form_data(
    sem: Semester = ...,
    deg: DegreeType = ...,
    cat: CourseCategory = ...,
    col: College = ...,
) -> Dict[str, str]: ...
def get_course_form_data(sem: Semester, dep: Department) -> Dict[str, str]: ...
