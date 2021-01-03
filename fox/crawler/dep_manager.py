from dataclasses import dataclass

from .type_parser import TypeParser, ParseType
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
import time
import json
from .Tool.progress import MyProgress as Progress


class DepManager:
    def __init__(self, sem: Semester, reuse: bool = True) -> None:
        self.nctu = NCTUAPI_Interactor()
        self.sem = sem
        self.reuse = reuse
        self.dep_dict: Dict[str, Department] = {}

    def run(self):
        if self.reuse:
            self.load_from_cache()
        if self.dep_dict == {}:
            self.load_from_crawl()

    def load_from_cache(self):
        # TODO : load_from_cache
        pass

    def load_from_crawl(self):
        with Progress(transient=True) as progress:
            self.prog = progress
            self.crawl(step=1)
            with open("dep_dict.json", "w") as fp:
                json_dict = {k: v.__dict__ for k, v in self.dep_dict.items()}
                json.dump(json_dict, fp, ensure_ascii=False)

    def crawl(self, step: int, **kwargs):
        func = {
            1: self.crawl_degree_type,
            2: self.crawl_course_category,
            3: self.crawl_college,
            4: self.crawl_department,
        }.get(step)
        func(step, **kwargs)

    def crawl_degree_type(self, step: int):
        degs = self.nctu.fetch_degree_type(self.sem)
        degs = TypeParser.parse(degs, DegreeType)
        for deg in self.prog.track(degs, description="[red]Crawl Degree Type..."):
            assert type(deg) is DegreeType
            self.crawl(step + 1, deg=deg)

    def crawl_course_category(self, step: int, **kwargs):
        cats = self.nctu.fetch_course_category(self.sem, **kwargs)
        cats = TypeParser.parse(cats, CourseCategory)
        for cat in self.prog.track(cats, description="[green]Crawl Course Category..."):
            assert type(cat) is CourseCategory
            self.crawl(step + 1, cat=cat, **kwargs)

    def crawl_college(self, step: int, deg: DegreeType, **kwargs):
        kwargs["deg"] = deg
        if deg.zh_name in ["研究所課程", "學士班課程"]:
            cols = self.nctu.fetch_colleges(self.sem, **kwargs)
            cols = TypeParser.parse(cols, College)
            for col in self.prog.track(cols, description="[cyan]Crawl College..."):
                assert type(col) is College
                self.crawl(step + 1, col=col, **kwargs)
        else:
            self.crawl(step + 1, col=College(), **kwargs)

    def crawl_department(self, step: int, **kwargs):
        deps = self.nctu.fetch_departments(self.sem, **kwargs)
        deps = TypeParser.parse(deps, Department)
        for dep in self.prog.track(deps, description="[blue]Crawl Department..."):
            assert type(dep) is Department
            if dep.uuid not in self.dep_dict:
                self.dep_dict[dep.uuid] = dep
                # print(f"callback: {dep}")
                time.sleep(0.1)

    def get_deps(self) -> Optional[List[Department]]:
        return list(self.dep_dict.values())
