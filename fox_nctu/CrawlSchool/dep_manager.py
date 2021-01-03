from dataclasses import dataclass

from .type_parser import TypeParser
from .objects import (
    DegreeType,
    Term,
    Semester,
    Department,
    Course,
    CourseCategory,
    College,
)
from typing import List, Dict, Optional, Union
from .nctu_api_nteractor import NCTUAPI_Interactor
from rich import print
from dataclasses import dataclass
import pprint


class DepManager:
    def __init__(self, sem: Semester, reuse: bool = True) -> None:
        self.nctu = NCTUAPI_Interactor()
        self.sem = sem
        self.reuse = reuse
        self.deps: Optional[List[Department]] = []
        self.run()

    def run(self):
        if self.reuse:
            self.deps = self.load_from_cache()
        if self.deps == []:
            self.deps = self.load_from_crawl()

    def load_from_cache(self):
        # TODO : load_from_cache
        pass

    def load_from_crawl(self):
        # TODO : load_from_crawl
        self.crawl_degree_type()

        pass

    def crawl_degree_type(self):
        degs = self.nctu.fetch_degree_type(self.sem)
        degs = TypeParser.parse(degs, DegreeType)
        for deg in degs:
            assert type(deg) is DegreeType
            self.crawl_course_category(deg)

    def crawl_course_category(self, deg: DegreeType):
        cats = self.nctu.fetch_course_category(self.sem, deg)
        cats = TypeParser.parse(cats, CourseCategory)
        for cat in cats:
            assert type(cat) is CourseCategory
            self.crawl_colleges(deg, cat)

    def crawl_colleges(self, deg: DegreeType, cat: CourseCategory):
        cols = self.nctu.fetch_colleges(self.sem, deg, cat)
        cols = TypeParser.parse(cols, College)
        for col in cols:
            assert type(col) is College
            self.crawl_departments(deg, cat, col)
        print(cols)

    def crawl_departments(self, deg: DegreeType, cat: CourseCategory, col: College):
        pass

    def get_deps(self) -> Optional[List[Department]]:
        return self.deps
