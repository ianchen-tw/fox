import json
import time
from collections import defaultdict
from dataclasses import asdict
from typing import Any, Dict, List, Union

import rich
from rich.progress import BarColumn, Progress, TextColumn

from fox.api.form_types import College, CourseCategory, DegreeType, Department
from fox.api.targets import (
    CatController,
    ColController,
    CrawlTarget,
    DegController,
    DepController,
)
from fox.cache import FoxCache
from fox.config import config
from fox.types import Semester

# Controller = Union[DegController, CatController, ColController, DepController]
Param = Union[Semester, DegreeType, CourseCategory, College, Department]


class DepManager:
    def __init__(self, sem: Semester, reuse: bool = True) -> None:
        self.sem = sem
        self.reuse = reuse
        self.dep_list: List[Department] = []

        self.cache = FoxCache(
            target_path=config.cache_base_folder_path
            / f"{sem}/{config.cache_dep_uuid_file_name}",
            encode_func=lambda dep_list: [asdict(dep) for dep in dep_list],
            decode_func=lambda data: [Department(**d) for d in data],
        )

    def run(self):
        if self.reuse:
            dep_list = self.cache.load()
            self.dep_list = dep_list if dep_list is not None else []

        if self.dep_list == []:
            self.load_from_crawl()
            self.cache.save(self.dep_list)

    def load_from_crawl(self):
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("[blue]{task.completed}/{task.total}"),
            TextColumn("(96)"),  # as for reference (109 first)
            transient=True,
        ) as progress:
            self.prog = progress
            self.total = 1
            self.task = progress.add_task(
                f"[red]Sem {str(self.sem)} Departments Crawl...", total=self.total
            )
            self.crawl(sem=self.sem)

    def create_controller(self, step: int, **kwargs) -> CrawlTarget:
        controller = {
            1: DegController,
            2: CatController,
            3: ColController,
            4: DepController,
        }.get(step)
        assert controller is not None
        return controller(**kwargs)

    def add_param(self, new_param: Param, step: int, **kwargs) -> Dict[str, Any]:
        param = {
            1: "deg",
            2: "cat",
            3: "col",
        }.get(step)
        assert param is not None
        kwargs[param] = new_param
        return kwargs

    def crawl(self, step: int = 1, **kwargs):
        controller: CrawlTarget = self.create_controller(step, **kwargs)
        controller.crawl()
        objects = controller.get_list()
        if objects and type(objects[0]) is not Department:
            self.total += len(objects)
        self.prog.update(self.task, total=self.total, advance=1)
        for object in objects:
            if type(object) is Department:
                self.dep_list.append(object)
                time.sleep(0.1)
            else:
                kwargs = self.add_param(object, step, **kwargs)
                self.crawl(step + 1, **kwargs)

    def get_deps(self) -> List[Department]:
        return self.dep_list

    def condense(self):
        """Clean dep_list data"""
        # may have duplicate department data
        # or multiple name for the same uuid (usually alias)

        def first_and_only(s: set):
            if len(s) > 1 or len(s) == 0:
                raise RuntimeError("input should only have one item")
            return next(iter(s))

        def dump_result(sem: Semester, dep_list: List[Department]):
            filename = f"./dep_{sem.year}_{sem.term}.py"
            with open(filename, "w", encoding="utf-8") as f:
                json_data = [asdict(dep) for dep in dep_list]
                code = "data = "
                code += json.dumps(json_data, indent="  ", ensure_ascii=False)
                f.write(code)

        uuid_2_names: Dict[str, set] = defaultdict(set)
        for dep in self.dep_list:
            uuid_2_names[dep.uuid].add(dep.name)

        result = []
        # TODO: add log for department with multiple deps/names
        for uuid, dep_names in uuid_2_names.items():
            dep: Department
            if len(dep_names) > 1:
                longest_desc = max(dep_names, key=lambda x: len(x))
                dep = Department(uuid=uuid, name=longest_desc)
            else:
                dep = Department(uuid=uuid, name=first_and_only(dep_names))
            result.append(dep)

        rich.print(result)

        dump_result(sem=self.sem, dep_list=result)
        # print(dic)
        # print("good")
