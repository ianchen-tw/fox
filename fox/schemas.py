import pprint
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict, Literal, Optional

from pydantic import BaseModel

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


@dataclass
class Department:
    uuid: str
    name: str

    def __str__(self) -> str:
        return f"{self.name}"


@dataclass
class DegreeType:
    """Undergrade, Graduate, PostDoc..."""

    uuid: str
    zh_name: str
    en_name: str


@dataclass
class CourseCategory:
    """Master, EMBA, inservice-masters"""

    code: str = "*"
    name: str = "not available"


@dataclass
class College:
    """Some department might not have college
    in these case this field would be
        code:'*'
        name:'*'
    """

    code: str = "*"
    name: str = "not available"


@dataclass
class Course:
    """Raw course data sent from NCTU timetable"""

    course_id: Optional[str] = None
    info: Optional[Dict[str, str]] = None
    tags: Dict[str, Any] = field(default_factory=dict)

    def dump(self) -> str:
        infos = []
        infos.append(f"course_id: {self.course_id}")
        infos.append("infos: " + pprint.pformat(self.info))
        infos.append("tags: " + pprint.pformat(self.tags))
        return "\n".join(infos)
