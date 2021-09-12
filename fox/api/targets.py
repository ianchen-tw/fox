import typing
from typing import Any, Dict, List, Union

from pydantic import BaseModel
from typing_extensions import Protocol

from fox.api.form_types import (
    CodedOptions,
    College,
    CourseCategory,
    DegreeType,
    Department,
)
from fox.types import Course, Semester
from .fetch import fetch, get_course_form_data, get_form_data
from .parse_course import RawFormat, SingleItemDict, parse_courses

JSONType = Union[str, None, Dict[str, Any], List[Any]]
# T = TypeVar("T")


class ParseException(Exception):
    pass


class CrawlTarget(Protocol):
    """Each CrawlTarget would only be used once"""

    def fetch(self):
        raise NotImplementedError

    def parse(self, json_data: JSONType):
        raise NotImplementedError

    def crawl(self):
        raise NotImplementedError

    def get_list(self):
        raise NotImplementedError


class ColController(CrawlTarget):
    def __init__(
        self,
        sem: Semester,
        deg: DegreeType,
        cat: CourseCategory,
    ) -> None:
        self.sem: Semester = sem
        self.deg: DegreeType = deg
        self.cat: CourseCategory = cat
        self.data_list: List[College] = []

    def crawl(self):
        if self.deg.zh_name in ["研究所課程", "學士班課程"]:
            json_data = self.fetch()
            self.data_list = self.parse(json_data)
        else:
            self.data_list = [College()]

    def fetch(self) -> JSONType:
        """Only when degree type equals to "master degree" or "undergrad"
        would have to query colleges.., and this is done by self.crawl()
        and in actual query dep api the college could leave as '*'
        """
        param = {"r": "main/get_college"}
        form_data = get_form_data(self.sem, self.deg, self.cat)
        res = fetch(param, form_data)
        return res

    def parse(self, json_data: JSONType):
        if type(json_data) == list:
            return [College()]
        assert isinstance(json_data, dict)
        options = CodedOptions.from_coded_dict(json_data)
        return [College(code=opt.code, name=opt.value) for opt in options]

    def get_list(self):
        return self.data_list


class CatController(CrawlTarget):
    def __init__(
        self,
        sem: Semester,
        deg: DegreeType,
    ) -> None:
        self.sem: Semester = sem
        self.deg: DegreeType = deg
        self.data_list: List[CourseCategory] = []

    def crawl(self):
        json_data = self.fetch()
        self.data_list = self.parse(json_data)

    def fetch(self) -> JSONType:
        param = {"r": "main/get_category"}
        form_data = get_form_data(self.sem, self.deg)
        res = fetch(param, form_data)
        return res

    def parse(self, json_data: JSONType):
        if type(json_data) == list:
            return [CourseCategory()]
        assert isinstance(json_data, dict)
        options = CodedOptions.from_coded_dict(json_data)
        result = [CourseCategory(code=opt.code, name=opt.value) for opt in options]
        return result

    def get_list(self):
        return self.data_list


class CourseController(CrawlTarget):
    def __init__(self, sem: Semester, dep: Department) -> None:
        self.sem: Semester = sem
        self.dep: Department = dep
        self.data_list: List[Course] = []

    def crawl(self):
        json_data = self.fetch()
        self.data_list = self.parse(json_data)

    def fetch(self) -> JSONType:
        param = {"r": "main/get_cos_list"}
        form_data = get_course_form_data(self.sem, self.dep)
        res = fetch(param, form_data)
        return res

    def parse(self, json_data: JSONType):
        if not json_data:
            return []
        json_data = typing.cast(Dict[str, Any], json_data)
        data = SingleItemDict(json_data).unpack()
        handle = RawFormat(**data)
        courses = parse_courses(handle)
        return courses

    def get_list(self):
        return self.data_list


class DegController(CrawlTarget):
    def __init__(self, sem: Semester) -> None:
        self.sem: Semester = sem
        self.data_list: List[DegreeType] = []

    def crawl(self):
        json_data = self.fetch()
        self.data_list = self.parse(json_data)

    def fetch(self) -> JSONType:
        param = {"r": "main/get_type"}
        form_data = get_form_data(self.sem)
        res = fetch(param, form_data)
        return res

    def parse(self, json_data: JSONType):
        assert isinstance(json_data, list)

        class RawRecord(BaseModel):
            uid: str
            cname: str  # chinese name
            ename: str  # english name

        raw_records = [RawRecord(**d) for d in json_data]
        return [
            DegreeType(uuid=r.uid, zh_name=r.cname.strip(), en_name=r.ename.strip())
            for r in raw_records
        ]

    def get_list(self):
        return self.data_list


class DepController(CrawlTarget):
    def __init__(
        self,
        sem: Semester,
        deg: DegreeType,
        cat: CourseCategory,
        col: College,
    ) -> None:
        self.sem: Semester = sem
        self.deg: DegreeType = deg
        self.cat: CourseCategory = cat
        self.col: College = col
        self.data_list: List[Department] = []

    def crawl(self):
        json_data = self.fetch()
        self.data_list = self.parse(json_data)

    def fetch(self) -> JSONType:
        param = {"r": "main/get_dep"}
        form_data = get_form_data(self.sem, self.deg, self.cat, self.col)
        res = fetch(param, form_data)
        return res

    def parse(self, json_data: JSONType):
        if type(json_data) != dict or not json_data:
            return []
        assert isinstance(json_data, dict)
        options = CodedOptions.from_coded_dict(json_data)
        result = [Department(uuid=opt.code, name=opt.value) for opt in options]
        return result

    def get_list(self):
        return self.data_list
