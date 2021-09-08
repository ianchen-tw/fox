from dataclasses import dataclass
from typing import TYPE_CHECKING

""" Contain raw data format that school accept/receive
"""

if TYPE_CHECKING:
    # add hint for code intellisense
    from dataclasses import dataclass as syntax_complete
else:

    def syntax_complete(model):
        return model


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
