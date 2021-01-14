from dataclasses import dataclass
from pprint import pprint
from typing import Any, Dict, List, Optional

from ..fetch import fetch, get_course_form_data, get_form_data
from ..objects import College, CourseCategory, DegreeType, Department, Semester
from .target_object_interface import I_TargetObject, JSONType


@dataclass
class Course:
    """Raw course data sent from NCTU timetable"""

    course_id: Optional[str] = None
    info: Optional[Dict] = None
    tags: Optional[Dict] = None

    def dump(self) -> str:
        infos = []
        infos.append(f"course_id: {self.course_id}")
        infos.append("infos: " + pprint.pformat(self.info))
        infos.append("tags: " + pprint.pformat(self.tags))
        return "\n".join(infos)


class CourseController(I_TargetObject):
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
        def get_first_value(data: Dict[str, Any]) -> Dict:
            return list(data.values())[0]

        if not json_data:
            return []

        assert type(json_data) is dict
        data = get_first_value(json_data)

        courses = {}

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
