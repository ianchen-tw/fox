import re
import typing
from decimal import Decimal
from typing import Any, Dict, List, NewType, Optional

from pydantic import BaseModel, Field

from fox.types import Course, CourseInfo

ApiCourseID = NewType("ApiCourseID", str)


class RawFormat(BaseModel):
    """API 針對單一 department 所回傳的原始資料格式
    其中，Field 中的 alias 參數代表原始資料格式中的名稱，因為太醜所以在這裡先做一次重新命名
    整體回傳的 API 邏輯很簡單，主要課程內容是由 main_courses + related_courses 中指定的課程所組成
    而單一課程的額外資訊會藉由其他欄位給出的資訊進行補足，比如說
    + brief 會放置關於單一課程的額外性質的簡稱，通常會是通識課程主題標籤(只用於顯示用途)
    + cos_type 放置單一課程有哪些額外的標籤以及相關性質
    我們在這裡不會使用到 brief 欄位，因為 cos_type 之中的資訊更為完整
    """

    main_courses: Optional[Dict[Any, Dict]] = Field(alias="1", description="課程")
    related_courses: Optional[Dict[Any, Dict]] = Field(alias="2", description="相關課程")
    dep_id: str
    dep_name_zh: str = Field(..., alias="dep_cname")
    dep_name_en: str = Field(..., alias="dep_ename")
    brief: Any  # 給顯示課程使用的摘要
    costype: Any  # 課程的附加屬性，可能是 通識，遠距課程 等等
    language: Any


class SingleItemDict:
    """A dict with one item inside it
    This is a data format get from api
    """

    def __init__(self, dic: Dict):
        self._dic = dic

    def unpack(self) -> Any:
        return list(self._dic.values())[0]


class CodedItems:
    """Manily used for documenting purpose"""

    def __init__(self, data: Dict):
        self._dic = {k: v for k, v in data.items()}

    @property
    def values(self):
        return [v for v in self._dic.values()]

    def __iter__(self):
        # name, item
        return iter([(k, v) for k, v in self._dic.items()])


class RawCourseInfo(BaseModel):
    academic_year: str = Field(..., alias="acy", description="學年")
    semester: str = Field(..., alias="sem", description="學期")
    course_number: str = Field(..., alias="cos_id", description="當期課號")
    perm_code: str = Field(..., alias="cos_code", description="永久課號")
    credits: str = Field(..., alias="cos_credit", description="學分數")
    dep_name_en: str = Field(..., alias="dep_ename", description="開課單位")
    dep_name_zh: str = Field(..., alias="dep_cname", description="開課單位(英文)")
    zh_name: str = Field(..., alias="cos_cname", description="課程名稱(中文)")
    en_name: str = Field(..., alias="cos_ename", description="課程名稱(英文)")
    num_limit: int = Field(..., alias="num_limit", description="註冊上限")
    num_registered: str = Field(..., alias="reg_num", description="註冊人數")
    teach_hours: str = Field(..., alias="cos_hours", description="授課時數")
    course_time: str = Field(..., alias="cos_time", description="課程時間/地點代碼")
    teacher: str = Field(..., description="授課講師")
    memo: Optional[str] = Field(description="備註")
    zh_type: str = Field(..., alias="cos_type", description="選別")
    en_type: str = Field(..., alias="cos_type_e", description="選別(英文)")
    # unknown fields
    link: Optional[str] = Field(alias="URL", description="未知")
    link_teacher: str = Field(..., alias="TURL", description="未知")
    crsoutline_type: Optional[str] = Field(description="未知")
    brief: str = Field(..., description="未知")
    dep_limit: str = Field(..., alias="dep_limit", description="未知")

    @property
    def api_id(self):
        """A unique identifier used in the API for indentifing courses"""
        return f"{self.academic_year}{self.semester}_{self.course_number}"

    def extract_base_info(self) -> Course:
        reg_limit: Optional[int] = self.num_limit if self.num_limit < 9000 else None
        memo = self.memo.strip() if self.memo is not None else ""

        info = CourseInfo(
            academic_year=int(self.academic_year),
            semester=self.semester,
            course_number=self.course_number,
            perm_code=self.perm_code.strip(),
            name_zh=self.zh_name.strip(),
            name_en=self.en_name.strip(),
            credits=Decimal(self.credits),
            register_limit=reg_limit,
            teach_hours=Decimal(self.teach_hours),
            course_time=self.course_time,
            teachers=self.teacher,
            type_zh=self.zh_type,
            type_en=self.en_type,
            memo=memo,
            dep_name_en=self.dep_name_en.strip(),
            dep_name_zh=self.dep_name_zh.strip(),
        )
        return Course(info=info, api_id=self.api_id)


def extract_course_info(data: RawFormat) -> List[RawCourseInfo]:
    raw_courses = []
    if data.main_courses is not None:
        main = CodedItems(data.main_courses).values
        raw_courses.extend(main)
    if data.related_courses is not None:
        related = CodedItems(data.related_courses).values
        raw_courses.extend(related)
    return [RawCourseInfo(**r) for r in raw_courses]


def extract_lang_tag(data: RawFormat) -> Dict[ApiCourseID, str]:
    res = {}
    for api_id, value in CodedItems(data.language):
        lang = SingleItemDict(value).unpack()
        res[api_id] = f"lang:{lang}"
    return res


def extract_type_tags(data: RawFormat) -> Dict[ApiCourseID, List[str]]:
    # 課程特色標籤 (遠距、通識)
    # tag 結構: fullName_shortName
    tag_full_name = re.compile(r"^(.+?)_")

    res = {}
    for api_id, coded_items in CodedItems(data.costype):
        tags = []
        for raw_tag, tag_detail in CodedItems(coded_items):
            match = tag_full_name.match(raw_tag)
            if not match:
                continue
            full_name = match.group(1)
            tags.append(full_name)
        if tags:
            res[api_id] = tags
    return res


def parse_courses(handle: RawFormat) -> List[Course]:

    tags_lang = extract_lang_tag(handle)
    tags_types = extract_type_tags(handle)
    info_courses = extract_course_info(handle)

    parsed: List[Course] = []
    for basic_info in info_courses:
        course = basic_info.extract_base_info()
        api_id = typing.cast(ApiCourseID, course.api_id)
        if api_id in tags_lang:
            lang_tag = tags_lang[api_id]
            course.tags.append(lang_tag)
        if api_id in tags_types:
            type_tags = tags_types[api_id]
            course.tags.extend(type_tags)
        parsed.append(course)
    return parsed


# def main():
#     data = SingleItemDict(raw_course_list).unpack()
#     handle = RawFormat(**data)

#     courses = parse_courses(handle)
#     for c in courses:
#         print(c.tags)
#     return
