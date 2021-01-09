from typing import List

from .cache import Cache
from .nctu_api_interactor import NCTUAPI_Interactor
from .objects import Course, Department, Semester
from .Tool.progress import MyProgress as Progress
from .type_parser import TypeParser


class CourseManager:
    def __init__(self, sem: Semester, dep: Department, reuse: bool = True) -> None:
        self.nctu = NCTUAPI_Interactor()
        self.sem = sem
        self.dep = dep
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
        courses = self.nctu.fetch_course_raw_data(self.sem, self.dep)
        courses = TypeParser.parse(courses, Course)
        for course in self.prog.track(courses, description="[yellow] Crawl Course..."):
            assert type(course) is Course
            if course not in self.course_list:
                self.course_list.append(course)

    def get_courses(self) -> List[Course]:
        return self.course_list
