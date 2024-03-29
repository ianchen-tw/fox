from typing import Dict

import httpx

from fox.config import config
from fox.types import JSONType, Semester
from .form_types import College, CourseCategory, DegreeType, Department


def fetch(param: Dict[str, str], form_data: Dict[str, str]) -> JSONType:
    retry_times = 0
    while retry_times < 3:
        try:
            res = httpx.post(config.timetable_url, params=param, data=form_data)
            return res.json()
        except httpx.ReadTimeout:
            retry_times += 1
    return []


def get_form_data(
    sem: Semester = None,
    deg: DegreeType = None,
    cat: CourseCategory = None,
    col: College = None,
) -> Dict[str, str]:
    form_data: Dict[str, str] = dict()
    form_data["flang"] = "zh-tw"
    if sem:
        form_data["acysem"] = str(sem)
        form_data["acysemend"] = str(sem)
    if deg:
        form_data["ftype"] = deg.uuid
    if cat:
        form_data["fcategory"] = cat.code
    if col:
        form_data["fcollege"] = col.code
    return form_data


def get_course_form_data(sem: Semester, dep: Department) -> Dict[str, str]:
    not_important = [
        "m_costype",
        "m_crsoutline",
        "m_crstime",
        "m_cos_code",
        "m_group",
        "m_grade",
        "m_class",
        "m_option",
        "m_crsname",
        "m_teaname",
        "m_cos_id",
    ]
    form_data = {
        # "flang": "zh-tw",
        "m_acy": str(sem.year),
        "m_sem": sem.term,
        "m_acyend": str(sem.year),
        "m_semend": sem.term,
        "m_dep_uid": dep.uuid,
        **{key: "**" for key in not_important},
    }
    return form_data
