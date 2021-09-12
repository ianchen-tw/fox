from fox.api.parse_course import (
    RawFormat,
    SingleItemDict,
    extract_lang_tag,
    extract_type_tags,
    parse_courses,
)
from .data import example_api_data


def test_smoke_parse():
    data = SingleItemDict(example_api_data.data).unpack()
    handle = RawFormat(**data)
    parse_courses(handle)


def test_single_item_dict_unpack():
    target = {"name": "ian", "age": 18}
    data = {"NotUsed": target.copy()}
    assert SingleItemDict(data).unpack() == target


def test_extract_lang():
    data = RawFormat(
        **{
            "1": {},
            "2": {},
            "dep_id": "",
            "dep_cname": "",
            "dep_ename": "",
            "language": {
                "1101_A010": {"授課語言代碼": "zh-tw"},
                "1101_B373": {"授課語言代碼": "en-us"},
            },
        }
    )
    expected = {"1101_A010": "lang:zh-tw", "1101_B373": "lang:en-us"}
    assert extract_lang_tag(data) == expected


def test_extract_type_tags():
    data = RawFormat(
        **{
            "1": {},
            "2": {},
            "dep_id": "",
            "dep_cname": "",
            "dep_ename": "",
            "costype": {
                # "1101_1143": {"": {}},
                "1101_1145": {
                    "博雅選修通識_博雅選修通識": {},
                    "基本素養-組織管理_基本素養-組織管理": {},
                },
                "1101_1147": {"遠距課程_遠距": {}},
            },
        }
    )
    expected = {"1101_1145": ["博雅選修通識", "基本素養-組織管理"], "1101_1147": ["遠距課程"]}
    assert extract_type_tags(data) == expected
