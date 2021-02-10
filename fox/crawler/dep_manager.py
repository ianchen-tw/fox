import json
import time
from dataclasses import asdict
from typing import Any, Dict, List, Union

from rich.progress import BarColumn, Progress, TextColumn

from . import cache
from .target_object.college import ColController
from .target_object.course_category import CatController
from .target_object.degree_type import DegController
from .target_object.department import DepController
from .target_object.meta_object import (
    College,
    CourseCategory,
    DegreeType,
    Department,
    Semester,
)
from .types import JSONType

Controller = Union[DegController, CatController, ColController, DepController]
Param = Union[Semester, DegreeType, CourseCategory, College, Department]


class DepManager:
    def __init__(self, sem: Semester, reuse: bool = True) -> None:
        self.sem = sem
        self.reuse = reuse
        self.dep_list: List[Department] = []
        self.save_path = cache.get_path() / str(sem) / "dep_uuid_list.json"

    def run(self):
        if self.reuse:
            self.load_from_cache()
        if self.dep_list == []:
            self.load_from_crawl()
            self.dump()

    def load_from_cache(self):
        try:
            with open(self.save_path, "r", encoding="utf-8") as fp:
                data: JSONType = json.load(fp)
                self.dep_list = [
                    Department(**d) for d in data if not isinstance(d, str)
                ]
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.dep_list = []

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

    def create_controller(self, step: int, **kwargs) -> Controller:
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
        controller = self.create_controller(step, **kwargs)
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

    def dump(self):
        self.save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.save_path, "w", encoding="utf-8") as fp:
            json_data = [asdict(dep) for dep in self.dep_list]
            json.dump(json_data, fp, indent="\t", ensure_ascii=False)

    def get_deps(self) -> List[Department]:
        return self.dep_list
