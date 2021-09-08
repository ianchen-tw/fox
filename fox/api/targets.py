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

JSONType = Union[str, None, Dict[str, Any], List[Any]]


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
        result = []
        if type(json_data) == list:
            return [College()]
        assert isinstance(json_data, dict)
        for key, value in json_data.items():
            if value:
                dic = {"code": key.strip(), "name": value.strip()}
                col = College(**dic)
            else:
                col = College()
            result.append(col)
        return result

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
        def get_first_value(data: Dict[str, Any]) -> Dict[str, Any]:
            return list(data.values())[0]

        if not json_data:
            return []

        assert isinstance(json_data, dict)
        data = get_first_value(json_data)

        courses: Dict[str, Course] = {}

        # TODO: refactor each steps into separated function
        # parse data["1"] and data["2"]
        for key in [k for k in ["1", "2"] if k in data]:
            # '1', '2' contains the main and related courses
            for course_id, val in data[key].items():
                # TODO: test that duplicate courses are the same
                courses[course_id] = Course(
                    **{
                        "course_id": course_id,
                        "info": val,
                        "tags": {},
                    }
                )
        # parse data["brief"]
        for course_id, brief in data["brief"].items():
            brief = get_first_value(brief).get("brief", "")
            if brief != "":
                courses[course_id].tags["brief"] = brief.split(",")

        # parse data["costype"]
        for course_id, cos_type_infos in data["costype"].items():
            for type_name, info in cos_type_infos.items():
                if type_name != "":
                    # create a list in courses[course_id].tags["cos_type"]
                    if None == courses[course_id].tags.get("cos_type", None):
                        courses[course_id].tags["cos_type"] = []
                    courses[course_id].tags["cos_type"].append(type_name)

        # parse data["language"]
        for course_id, teach_lang in data["language"].items():
            teach_lang = get_first_value(teach_lang)
            courses[course_id].tags["teach_lang"] = teach_lang

        return list(courses.values())

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
