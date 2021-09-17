from decimal import Decimal
from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional, Union

from attr import attrib, attrs
from pydantic import BaseModel

JSONType = Union[str, None, Dict[str, Any], List[Any]]

if TYPE_CHECKING:
    # add hint for code intellisense
    from dataclasses import dataclass as syntax_complete
else:

    def syntax_complete(model):
        return model


@syntax_complete
class Semester(BaseModel):
    year: int

    # 1: first
    # 2: second
    # X: summer
    term: Literal["1", "2", "X"]

    def __str__(self) -> str:
        return f"{self.year}{self.term}"


@attrs
class ClassTime:
    time_code: int  # 時間(Weekday+timeslot)
    room_code: str  # 教室代碼
    loc_code: Optional[str]  # 校區代碼


@attrs(auto_attribs=True, repr=True, str=True)
class CourseInfo:
    academic_year: int
    semester: str
    dep_name_en: str
    dep_name_zh: str
    course_number: str
    perm_code: str
    credits: Decimal
    register_limit: Optional[int]
    # todo: convert to classTime
    course_time: str
    teachers: str
    teach_hours: Decimal
    type_zh: str
    type_en: str
    name_zh: str
    name_en: str
    memo: str


@attrs(auto_attribs=True, repr=True, str=True)
class Course:
    # Basic information
    info: CourseInfo

    # the id used by the identifier
    api_id: str

    # Some auxiliary data
    tags: List[str] = attrib(factory=list)

    @classmethod
    def from_dict(cls, *args, **kwargs):
        _info = kwargs["info"]
        info = CourseInfo(**_info)
        return cls(info=info, api_id=kwargs["api_id"], tags=kwargs["tags"])
        pass
