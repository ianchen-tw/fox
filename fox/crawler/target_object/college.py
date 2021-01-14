from dataclasses import dataclass
from typing import List

from ..fetch import fetch, get_form_data
from ..objects import College, CourseCategory, DegreeType, Semester
from .target_object_interface import I_TargetObject, JSONType


@dataclass
class College:
    """Some department might not have college
    in these case this field would be
        code:'*'
        name:'*'
    """

    code: str = "*"
    name: str = "not available"


class ColController(I_TargetObject):
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
        would have to query colleges..
        and in actual query dep api the college could leave as '*'
        """
        # TODO: we have to detect the deg type in outer loop code and not query at all
        param = {"r": "main/get_college"}
        form_data = get_form_data(self.sem, self.deg, self.cat)
        res = fetch(param, form_data)
        return res.json()

    def parse(self, json_data: JSONType):
        result = []
        if type(json_data) == list:
            return [College()]
        assert type(json_data) is dict
        for key, value in json_data.items():
            # TODO: we shouldn't handle this error at all,
            # Instead, we should not call this method ( or just return a dummy college object)
            # the degree type is not master or undergrad
            if value:
                dic = {"code": key.strip(), "name": value.strip()}
                col = College(**dic)
            else:
                col = College()
            result.append(col)
        return result

    def get_list(self):
        return self.data_list
