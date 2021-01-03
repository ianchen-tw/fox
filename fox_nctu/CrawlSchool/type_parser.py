from typing import Any, Union, List, Type, Dict
from .objects import Term, Semester, DegreeType, CourseCategory, College, Department
import pprint

ParseType = Union[DegreeType, CourseCategory, College, Department]
ReturnParseType = Union[
    List[DegreeType], List[CourseCategory], List[College], List[Department]
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