import pprint
from typing import Any, Dict, List, Type, Union

from .objects import College, Course, CourseCategory, DegreeType, Department

ParseType = Union[DegreeType, CourseCategory, College, Department, Course]
ReturnParseType = Union[
    List[DegreeType],
    List[CourseCategory],
    List[College],
    List[Department],
    List[Course],
]


class ParseException(Exception):
    pass


# TODO : restructure the parser


class TypeParser:
    @staticmethod
    def parse(json_data: Any, parse_type: Type[ParseType]) -> ReturnParseType:
        func = {
            DegreeType: TypeParser.parse_degree_type,
            CourseCategory: TypeParser.parse_course_category,
            College: TypeParser.parse_college,
            Department: TypeParser.parse_department,
            Course: TypeParser.parse_course,
        }.get(parse_type, lambda x: [])
        return func(json_data)

    @staticmethod
    def parse_degree_type(json_data: Any) -> List[DegreeType]:
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

    @staticmethod
    def parse_course_category(json_data: Any) -> List[CourseCategory]:
        if type(json_data) == list:
            return [CourseCategory(**{"code": "*", "name": "not avaiable"})]

        result = []
        for key, value in json_data.items():
            if value:
                dic = {"code": key.strip(), "name": value.strip()}
            else:
                dic = {"code": "*", "name": "not avaiable"}
            result.append(CourseCategory(**dic))
        return result

    @staticmethod
    def parse_college(json_data: Any) -> List[College]:
        result = []
        if type(json_data) == list:
            return [College(**{"code": "*", "name": "not avaiable"})]

        for key, value in json_data.items():
            # TODO: we shouldn't handle this error at all,
            # Instead, we should not call this method ( or just return a dummy college object)
            # the degree type is not master or undergrad
            if value:
                dic = {"code": key.strip(), "name": value.strip()}
            else:
                dic = {"code": "*", "name": "not avaiable"}
            result.append(College(**dic))
        return result

    @staticmethod
    def parse_department(json_data: Any) -> List[Department]:
        if type(json_data) != dict or not json_data:
            return []
        result = []
        for key, value in json_data.items():
            if value:
                dic = {"uuid": key.strip(), "name": value.strip()}
                result.append(Department(**dic))
        return result

    @staticmethod
    def parse_course(json_data: Any) -> List[Course]:
        def get_first_value(data: Dict[str, Any]) -> Dict:
            return list(data.values())[0]

        if not json_data:
            return []

        data = get_first_value(json_data)

        courses = {}
        # parse data["1"] and data["2"]
        for key in [k for k in ["1", "2"] if k in data]:
            # '1', '2' contains the main and related courses
            for course_id, val in data[key].items():
                if course_id not in courses:
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
