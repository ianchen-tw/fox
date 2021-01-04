from .crawler.crawler import Crawler
from .crawler.objects import Semester, Term


def main():
    semester = Semester(year=109, term=Term.FIRST)
    get_all_course(semester)


def get_all_course(sem: Semester):
    _ = Crawler.get_deps(sem=sem, reuse=False)
    # for dep in deps:
    #     courses = Crawler.get_courses(sem=sem, dep=dep)
    #     for course in courses:
    #         print(course)


if __name__ == "__main__":
    main()
