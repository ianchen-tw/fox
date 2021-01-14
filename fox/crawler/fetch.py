from typing import Dict

import httpx

from .objects import College, CourseCategory, DegreeType, Semester


def fetch(param: Dict[str, str], form_data: Dict[str, str]):
    url: str = "https://timetable.nctu.edu.tw/"
    return httpx.post(url, params=param, data=form_data)


def get_form_data(
    sem: Semester = None,
    deg: DegreeType = None,
    cat: CourseCategory = None,
    col: College = None,
):
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
