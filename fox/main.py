from typing import List

from rich.progress import track
from rich.traceback import install

from fox.course_manager import CourseManager
from fox.dep_manager import DepManager
from fox.schemas import Course, Department, Semester


def main():
    install(show_locals=True)

    # sem = Semester(year=108, term=Term.SECOND)
    # data = cache_get_deps(sem)
    # print(data)
    # return

    # for year in [107, 108, 109]:
    #     for term in [Term.FIRST, Term.SECOND, Term.SUMMER]:
    year = 108
    term = "1"
    sem = Semester(year=year, term=term)
    deps = get_deps(sem=sem, reuse=True)
    # _ = get_courses(sem=sem, deps=deps)
    print("finish")
    # print(courses)
    #     for course in courses:
    #         print(course)


def get_deps(sem: Semester, reuse: bool = True) -> List[Department]:
    dep_manager = DepManager(sem, reuse)
    dep_manager.run()
    deps = dep_manager.get_deps()
    dep_manager.condense()
    return deps


def get_courses(
    sem: Semester, deps: List[Department], reuse: bool = True
) -> List[Course]:
    courses: List[Course] = []
    for dep in track(deps, transient=True, description="[yellow] Crawl Course..."):
        course_manager = CourseManager(sem, dep, reuse)
        course_manager.run()
        courses.extend(course_manager.get_courses())
    return courses


if __name__ == "__main__":
    main()
