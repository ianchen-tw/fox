import pprint
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class Term(Enum):
    FIRST = "1"
    SECOND = "2"
    SUMMER = "X"


@dataclass
class Semester:
    year: int
    term: Term

    def __str__(self) -> str:
        return f"{self.year}{self.term.value}"


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
