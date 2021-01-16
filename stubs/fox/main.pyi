from typing import Any

from .crawler.crawler import Crawler as Crawler
from .crawler.target_object.meta_object import Semester as Semester
from .crawler.target_object.meta_object import Term as Term

def main() -> None: ...
def get_all_course(sem: Semester) -> Any: ...
