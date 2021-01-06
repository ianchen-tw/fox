from ..objects import Semester, Term
from ..nctu_api_interactor import NCTUAPI_Interactor
from rich import print


def test_fetch_degree_type():
    semester = Semester(year=109, term=Term.FIRST)
    nctu = NCTUAPI_Interactor()
    degree_types = nctu.fetch_degree_type(semester)
    assert type(degree_types) is list
    for degree_type in degree_types:
        degree_type["uid"]
        degree_type["cname"]
        degree_type["ename"]