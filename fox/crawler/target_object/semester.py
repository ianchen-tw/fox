from dataclasses import dataclass
from enum import Enum


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