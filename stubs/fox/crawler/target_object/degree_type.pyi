from typing import Any

from ..fetch import fetch as fetch
from ..fetch import get_form_data as get_form_data
from ..parse import ParseException as ParseException
from .meta_object import DegreeType as DegreeType
from .meta_object import Semester as Semester
from .target_object_interface import I_TargetObject as I_TargetObject
from .target_object_interface import JSONType as JSONType

class DegController(I_TargetObject):
    sem: Any = ...
    data_list: Any = ...
    def __init__(self, sem: Semester) -> None: ...
    def crawl(self) -> None: ...
    def fetch(self) -> JSONType: ...
    def parse(self, json_data: JSONType) -> Any: ...
    def get_list(self): ...