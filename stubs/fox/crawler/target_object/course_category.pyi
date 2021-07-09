from typing import Any

from ..fetch import fetch as fetch
from ..fetch import get_form_data as get_form_data
from .meta_object import CourseCategory as CourseCategory
from .meta_object import DegreeType as DegreeType
from .meta_object import Semester as Semester
from .target_object_interface import CrawlTarget as CrawlTarget
from .target_object_interface import JSONType as JSONType

class CatController(CrawlTarget):
    sem: Any = ...
    deg: Any = ...
    data_list: Any = ...
    def __init__(self, sem: Semester, deg: DegreeType) -> None: ...
    def crawl(self) -> None: ...
    def fetch(self) -> JSONType: ...
    def parse(self, json_data: JSONType) -> Any: ...
    def get_list(self): ...
