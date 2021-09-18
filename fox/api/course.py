from typing import List

from attr import asdict, attrib, attrs

from fox.api.form_types import Department
from fox.api.targets import CourseController
from fox.cache import FoxCache
from fox.types import Course, Semester
from fox.util import get_cache_path


@attrs(auto_attribs=True)
class CourseManager:
    sem: Semester
    dep: Department
    reuse: bool = True
    course_list: List[Course] = attrib(factory=list)

    def __attrs_post_init__(self):
        self.cache = FoxCache(
            target_path=get_cache_path() / f"{self.sem}/course/{self.dep.name}.json",
            encode_func=lambda courses: [asdict(c) for c in courses],
            decode_func=lambda data: [Course.from_dict(**d) for d in data],
        )

    def run(self):
        if self.reuse is True:
            course_list = self.cache.load()
            self.course_list = course_list if course_list is not None else []
        if self.course_list == []:
            self.load_from_crawl()
            self.cache.save(self.course_list)
        return self

    def load_from_crawl(self):
        self.crawl_course()

    def crawl_course(self):
        course_controller = CourseController(self.sem, self.dep)
        course_controller.crawl()
        for course in course_controller.get_list():
            if course not in self.course_list:
                self.course_list.append(course)
        return self

    def get_courses(self) -> List[Course]:
        return self.course_list
