from typing import List

from .target_object.meta_object import Course, Department, Semester

from .cache import Cache
from .target_object.course import CourseController
from .Tool.progress import MyProgress as Progress


class CourseManager:
    def __init__(self, sem: Semester, dep: Department, reuse: bool = True) -> None:
        self.sem: Semester = sem
        self.dep: Department = dep
        self.reuse = reuse
        self.course_list: List[Course] = []

    def run(self):
        if self.reuse:
            self.course_list = Cache.course_load(self.sem, self.dep)
        if self.course_list == []:
            self.load_from_crawl()

    def load_from_crawl(self):
        with Progress(transient=True) as progress:
            self.prog = progress
            self.prog = progress
            self.crawl_course()
            Cache.course_dump(self.sem, self.dep, self.course_list)

    def crawl_course(self):
        course_controller = CourseController(self.sem, self.dep)
        course_controller.crawl()
        for course in self.prog.track(
            course_controller.get_list(), description="[yellow] Crawl Course..."
        ):
            if course not in self.course_list:
                self.course_list.append(course)

    def get_courses(self) -> List[Course]:
        return self.course_list
