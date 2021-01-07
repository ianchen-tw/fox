from rich import print

from ..nctu_api_interactor import NCTUAPI_Interactor
from ..objects import College, CourseCategory, DegreeType, Semester, Term


def get_nctu():
    return NCTUAPI_Interactor()


def get_semester():
    return Semester(year=109, term=Term.FIRST)


def get_degree_type():
    dic = {
        "uuid": "870A5373-5B3A-415A-AF8F-BB01B733444F",
        "zh_name": "學士班課程",
        "en_name": "Undergraduate courses",
    }
    return DegreeType(**dic)


def get_course_category():
    return CourseCategory(code="3*", name="一般學士班")


def get_college():
    return College(code="I", name="電機學院")


def test_fetch_degree_type():
    nctu = get_nctu()
    semester = get_semester()
    degree_types = nctu.fetch_degree_type(semester)
    assert type(degree_types) is list
    for degree_type in degree_types:
        degree_type["uid"]
        degree_type["cname"]
        degree_type["ename"]


def test_fetch_course_category():
    nctu = get_nctu()
    sem = get_semester()
    deg = get_degree_type()
    cat = nctu.fetch_course_category(sem, deg)
    assert cat == {"3*": "一般學士班"}


def test_fetch_colleges():
    nctu = get_nctu()
    sem = get_semester()
    deg = get_degree_type()
    cat = get_course_category()
    col = nctu.fetch_colleges(sem, deg, cat)
    print(col)
    expect = {
        "I": "電機學院",
        "Z": "前瞻系統工程教育院",
        "C": "資訊學院",
        "E": "工學院",
        "S": "理學院",
        "M": "管理學院",
        "B": "生物科技學院",
        "A": "人文社會學院",
        "K": "客家文化學院",
        "Y": "電機與資訊學院",
    }
    assert col == expect


def test_fetch_departments():
    nctu = get_nctu()
    sem = get_semester()
    deg = get_degree_type()
    cat = get_course_category()
    col = get_college()
    dep = nctu.fetch_departments(sem, deg, cat, col)
    expect = {
        "CCF66C6B-573F-4C59-B03F-EEB6DE3FF989": "DCE(電機學院院級(學士班))",
        "049C687B-46BD-4E42-9A12-1D54874477A0": "DEE(電子工程學系)",
        "2F76991A-211C-4D75-B046-335E65EAE656": "DEO(光電工程學系)",
        "F25F72ED-9F1C-469A-A174-6FF0F0367955": "ECE(電機資訊學士班)",
        "73CEC435-74FF-49FE-88E7-63F369B3A3C5": "UEE(電機工程學系)",
    }
    assert dep == expect
