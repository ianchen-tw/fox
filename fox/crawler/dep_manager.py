import time
from typing import List, Optional

from .target_object.meta_object import Department, Semester

from .cache import Cache
from .target_object.college import ColController
from .target_object.course_category import CatController
from .target_object.degree_type import DegController
from .target_object.department import DepController
from .Tool.progress import MyProgress as Progress


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
            self.crawl(step=1)
            Cache.dep_dump(self.sem, self.get_deps())

    def crawl(self, step: int, **kwargs):
        func = {
            1: self.crawl_degree_type,
            2: self.crawl_course_category,
            3: self.crawl_college,
            4: self.crawl_department,
        }.get(step)
        func(step, **kwargs)

    def crawl_degree_type(self, step: int):
        deg_controller = DegController(self.sem)
        deg_controller.crawl()
        for deg in self.prog.track(
            deg_controller.get_list(), description="[red]Crawl Degree Type..."
        ):
            self.crawl(step + 1, deg=deg)

    def crawl_course_category(self, step: int, **kwargs):
        cat_controller = CatController(self.sem, **kwargs)
        cat_controller.crawl()
        for cat in self.prog.track(
            cat_controller.get_list(), description="[green]Crawl Course Category..."
        ):
            self.crawl(step + 1, cat=cat, **kwargs)

    def crawl_college(self, step: int, **kwargs):
        col_controller = ColController(self.sem, **kwargs)
        col_controller.crawl()
        for col in self.prog.track(
            col_controller.get_list(), description="[cyan]Crawl College..."
        ):
            self.crawl(step + 1, col=col, **kwargs)

    def crawl_department(self, step: int, **kwargs):  # noqa
        # TODO: congestion control, makesure we respect the server
        dep_controller = DepController(self.sem, **kwargs)
        dep_controller.crawl()
        for dep in self.prog.track(
            dep_controller.get_list(), description="[blue]Crawl Department..."
        ):
            if dep not in self.dep_list:
                self.dep_list.append(dep)
                time.sleep(0.1)

    def get_deps(self) -> Optional[List[Department]]:
        return self.dep_list
