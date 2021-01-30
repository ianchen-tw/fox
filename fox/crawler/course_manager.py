import json
from typing import List

from . import cache
from .target_object.course import CourseController
from .target_object.meta_object import Course, Department, Semester
from .Tool.progress import MyProgress as Progress
from .types import JSONType


class CourseManager:
    def __init__(self, sem: Semester, dep: Department, reuse: bool = True) -> None:
        self.sem: Semester = sem
        self.dep: Department = dep
        self.reuse = reuse
        self.course_list: List[Course] = []
        self.save_path = cache.get_path() / str(sem) / "course" / f"{str(dep)}.json"

    def run(self):
        if self.reuse:
            self.load_from_cache()
        if self.course_list == []:
            self.load_from_crawl()
            self.dump()

    def load_from_cache(self):
        try:
            with open(self.save_path, "rb") as fp:
                data: JSONType = json.load(fp)
                self.course_list = [Course(**d) for d in data]
        except FileNotFoundError:
            self.course_list = []

    def load_from_crawl(self):
        self.crawl_course()

    def crawl_course(self):
        course_controller = CourseController(self.sem, self.dep)
        course_controller.crawl()
        for course in course_controller.get_list():
            if course not in self.course_list:
                self.course_list.append(course)

    def dump(self):
        self.save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.save_path, "w", encoding="utf-8") as fp:
            json_data = [course.__dict__ for course in self.course_list]
            json.dump(json_data, fp, indent="\t", ensure_ascii=False)

    def get_courses(self) -> List[Course]:
        return self.course_list
