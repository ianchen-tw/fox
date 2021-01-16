import pprint
from typing import List

from ..fetch import fetch, get_form_data
from ..parse import ParseException
from .meta_object import DegreeType, Semester
from .target_object_interface import I_TargetObject, JSONType


class DegController(I_TargetObject):
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
        result = []
        for d in json_data:
            try:
                dic = {
                    "uuid": d["uid"],
                    "zh_name": d["cname"].strip(),
                    "en_name": d["ename"].strip(),
                }
                result.append(DegreeType(**dic))
            except KeyError as e:
                info = [
                    f"DegreeTypeParser/ unable to get key({e}) in data",
                    pprint.pformat(json_data, indent=4),
                ]
                raise ParseException("\n".join(info))
        return result

    def get_list(self):
        return self.data_list
