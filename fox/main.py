from .crawler.crawler import Crawler
from .crawler.objects import Semester, Term


def main():
    # install(show_locals=True)
    # for year in [107, 108, 109]:
    #     for term in [Term.FIRST, Term.SECOND, Term.SUMMER]:
    year = 109
    term = Term.FIRST
    semester = Semester(year=year, term=term)
    get_all_course(semester)


def get_all_course(sem: Semester):
    deps = Crawler.get_deps(sem=sem, reuse=True)
    for dep in deps:
        _ = Crawler.get_courses(sem=sem, dep=dep)
        # print(courses)
    #     for course in courses:
    #         print(course)


if __name__ == "__main__":
    main()
