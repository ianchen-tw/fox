from typing import List, Optional

from rich.progress import track
from rich.traceback import install

from fox.api.course import CourseManager
from fox.api.dep import DepManager
from fox.api.form_types import Department
from fox.types import Course, Semester


def main():
    install(show_locals=True)

    # sem = Semester(year=108, term=Term.SECOND)
    # data = cache_get_deps(sem)
    # print(data)
    # return

    # for year in [107, 108, 109]:
    #     for term in [Term.FIRST, Term.SECOND, Term.SUMMER]:
    year = 110
    term = "1"
    sem = Semester(year=year, term=term)
    _deps = get_deps(sem=sem, reuse=True)
    _courses = get_courses(sem=sem, deps=_deps, limit_deps=["(醫學系)"])
    print("finish")
    print(_courses)
    for course in _courses:
        print(course)


def get_deps(sem: Semester, reuse: bool = True) -> List[Department]:
    dep_manager = DepManager(sem, reuse)
    dep_manager.run()
    deps = dep_manager.get_deps()
    dep_manager.condense()
    return deps


def get_courses(
    sem: Semester,
    deps: List[Department],
    limit_deps: Optional[List[str]] = None,
    reuse: bool = True,
) -> List[Course]:
    courses: List[Course] = []

    if limit_deps is not None:
        deps = [dep for dep in deps if (dep.name in limit_deps)]

    for dep in track(deps, transient=True, description="[yellow] Crawl Course..."):
        course_manager = CourseManager(sem, dep, reuse)
        course_manager.run()
        courses.extend(course_manager.get_courses())
    return courses


if __name__ == "__main__":
    main()
