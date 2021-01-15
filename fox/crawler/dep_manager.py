import time
from typing import Any, Dict, List, Optional, Union

from .cache import Cache
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
from .Tool.progress import MyProgress as Progress

Controller = Union[DegController, CatController, ColController, DepController]
Param = Union[Semester, DegreeType, CourseCategory, College, Department]


class DepManager:
    def __init__(self, sem: Semester, reuse: bool = True) -> None:
        self.sem = sem
        self.reuse = reuse
        self.dep_list: List[Department] = []

    def run(self):
        if self.reuse:
            self.dep_list = Cache.dep_load(self.sem)
        if self.dep_list == []:
            self.load_from_crawl()

    def load_from_crawl(self):
        with Progress(transient=True) as progress:
            self.prog = progress
            self.crawl(sem=self.sem)
            Cache.dep_dump(self.sem, self.get_deps())

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
        for object in self.prog.track(controller.get_list()):
            if type(object) is Department:
                self.dep_list.append(object)
                time.sleep(0.1)
            else:
                kwargs = self.add_param(object, step, **kwargs)
                self.crawl(step + 1, **kwargs)

    def get_deps(self) -> Optional[List[Department]]:
        return self.dep_list
