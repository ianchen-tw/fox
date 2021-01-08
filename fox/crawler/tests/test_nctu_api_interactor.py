from dataclasses import dataclass
from typing import Dict, List

import pytest

from ..nctu_api_interactor import NCTUAPI_Interactor
from ..objects import College, CourseCategory, DegreeType, Semester, Term


@dataclass
class QueryTarget:
    sem: Semester = Semester(year=109, term=Term.FIRST)
    deg: DegreeType = DegreeType(
        **{
            "uuid": "870A5373-5B3A-415A-AF8F-BB01B733444F",
            "zh_name": "學士班課程",
            "en_name": "Undergraduate courses",
        }
    )
    cat: CourseCategory = CourseCategory(code="3*", name="一般學士班")
    col: College = College(code="I", name="電機學院")


@pytest.fixture(scope="session")
def query() -> QueryTarget:
    return QueryTarget()


@pytest.fixture
def nctu() -> NCTUAPI_Interactor:
    return NCTUAPI_Interactor()


def test_fetch_degree_type(nctu: NCTUAPI_Interactor, query: QueryTarget):
    degree_types: List[Dict] = nctu.fetch_degree_type(query.sem)
    assert type(degree_types) is list
    assert {
        "uid": "870A5373-5B3A-415A-AF8F-BB01B733444F",
        "type": "1",
        "cname": "學士班課程",
        "ename": "Undergraduate courses",
    } in degree_types


def test_fetch_course_category(nctu: NCTUAPI_Interactor, query: QueryTarget):
    cat = nctu.fetch_course_category(query.sem, query.deg)
    assert cat == {"3*": "一般學士班"}


def test_fetch_colleges(nctu: NCTUAPI_Interactor, query: QueryTarget):
    colleges = nctu.fetch_colleges(query.sem, query.deg, query.cat)
    assert colleges == {
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


def test_fetch_departments(nctu: NCTUAPI_Interactor, query: QueryTarget):
    departments = nctu.fetch_departments(query.sem, query.deg, query.cat, query.col)
    assert departments == {
        "CCF66C6B-573F-4C59-B03F-EEB6DE3FF989": "DCE(電機學院院級(學士班))",
        "049C687B-46BD-4E42-9A12-1D54874477A0": "DEE(電子工程學系)",
        "2F76991A-211C-4D75-B046-335E65EAE656": "DEO(光電工程學系)",
        "F25F72ED-9F1C-469A-A174-6FF0F0367955": "ECE(電機資訊學士班)",
        "73CEC435-74FF-49FE-88E7-63F369B3A3C5": "UEE(電機工程學系)",
    }
