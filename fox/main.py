from typing import List

from .crawler.course_manager import CourseManager
from .crawler.dep_manager import DepManager
from .crawler.target_object.meta_object import Course, Department, Semester, Term


def main():
    # install(show_locals=True)
    # for year in [107, 108, 109]:
    #     for term in [Term.FIRST, Term.SECOND, Term.SUMMER]:
    year = 109
    term = Term.FIRST
    semester = Semester(year=year, term=term)
    get_all_course(semester)


def get_all_course(sem: Semester):
    deps = get_deps(sem=sem, reuse=True)
    for dep in deps:
        _ = get_courses(sem=sem, dep=dep)
    print("finish")
    # print(courses)
    #     for course in courses:
    #         print(course)


def get_deps(sem: Semester, reuse: bool = True) -> List[Department]:
    dep_manager = DepManager(sem, reuse)
    dep_manager.run()
    deps = dep_manager.get_deps()
    return deps


def get_courses(sem: Semester, dep: Department, reuse: bool = True) -> List[Course]:
    course_manager = CourseManager(sem, dep, reuse)
    course_manager.run()
    courses = course_manager.get_courses()
    return courses


if __name__ == "__main__":
    main()
