from typing import List

from ..fetch import fetch, get_form_data
from .meta_object import College, CourseCategory, DegreeType, Department, Semester
from .target_object_interface import CrawlTarget, JSONType


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
        result = []
        for key, value in json_data.items():
            if value:
                dic = {"uuid": key.strip(), "name": value.strip()}
                result.append(Department(**dic))
        return result

    def get_list(self):
        return self.data_list
