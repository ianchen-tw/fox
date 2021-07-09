from typing import List

from ..fetch import fetch, get_form_data
from .meta_object import College, CourseCategory, DegreeType, Semester
from .target_object_interface import CrawlTarget, JSONType


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
