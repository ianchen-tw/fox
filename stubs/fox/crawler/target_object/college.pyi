from typing import Any

from ..fetch import fetch as fetch
from ..fetch import get_form_data as get_form_data
from .meta_object import College as College
from .meta_object import CourseCategory as CourseCategory
from .meta_object import DegreeType as DegreeType
from .meta_object import Semester as Semester
from .target_object_interface import CrawlTarget as CrawlTarget
from .target_object_interface import JSONType as JSONType

class ColController(CrawlTarget):
    sem: Any = ...
    deg: Any = ...
    cat: Any = ...
    data_list: Any = ...
    def __init__(self, sem: Semester, deg: DegreeType, cat: CourseCategory) -> None: ...
    def crawl(self) -> None: ...
    def fetch(self) -> JSONType: ...
    def parse(self, json_data: JSONType) -> Any: ...
    def get_list(self): ...
