from ..objects import College, CourseCategory, DegreeType, Department
from ..type_parser import TypeParser


def test_parse_degree_type():
    json_data = [
        {
            "uid": "870A5373-5B3A-415A-AF8F-BB01B733444F",
            "type": "1",
            "cname": "學士班課程",
            "ename": "Undergraduate courses",
        },
        {
            "uid": "D8E6F0E8-126D-4C2F-A0AC-F9A96A5F6D5D",
            "type": "2",
            "cname": "研究所課程",
            "ename": "Graduate courses",
        },
    ]
    expect_data = [
        DegreeType(
            uuid="870A5373-5B3A-415A-AF8F-BB01B733444F",
            zh_name="學士班課程",
            en_name="Undergraduate courses",
        ),
        DegreeType(
            uuid="D8E6F0E8-126D-4C2F-A0AC-F9A96A5F6D5D",
            zh_name="研究所課程",
            en_name="Graduate courses",
        ),
    ]
    degree_types = TypeParser.parse(json_data, DegreeType)
    assert degree_types == expect_data


def test_parse_course_category():
    json_data = {
        "2*": "一般研究所",
        "60A7936E-B0C0-4C0F-9DE7-33D16A367F20": "台中一中科學班",
        "": None,
    }
    expect_data = [
        CourseCategory(code="2*", name="一般研究所"),
        CourseCategory(code="60A7936E-B0C0-4C0F-9DE7-33D16A367F20", name="台中一中科學班"),
        CourseCategory(code="*", name="not avaiable"),
    ]
    course_categorys = TypeParser.parse(json_data, CourseCategory)
    assert course_categorys == expect_data


def test_parse_college():
    json_data = {
        "A": "人文社會學院",
        "B": "生物科技學院",
    }
    expect_data = [
        College(code="A", name="人文社會學院"),
        College(code="B", name="生物科技學院"),
    ]
    colleges = TypeParser.parse(json_data, College)
    assert colleges == expect_data


def test_parse_department():
    json_data = {
        "16F59D39-254D-4EE9-B742-6E9EF801F297": "DFL(外國語文學系)",
        "3CEF1CCE-9A5D-4B91-AA06-C3F717F7619E": "DOH(人文社會學院院本部)",
    }
    expect_data = [
        Department(uuid="16F59D39-254D-4EE9-B742-6E9EF801F297", name="DFL(外國語文學系)"),
        Department(uuid="3CEF1CCE-9A5D-4B91-AA06-C3F717F7619E", name="DOH(人文社會學院院本部)"),
    ]
    departments = TypeParser.parse_department(json_data)
    assert departments == expect_data
