from typing import List

from ..fetch import fetch, get_form_data
from .meta_object import CourseCategory, DegreeType, Semester
from .target_object_interface import CrawlTarget, JSONType


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
        result = []
        for key, value in json_data.items():
            if value:
                dic = {"code": key.strip(), "name": value.strip()}
                cat = CourseCategory(**dic)
            else:
                cat = CourseCategory()
            result.append(cat)
        return result

    def get_list(self):
        return self.data_list
