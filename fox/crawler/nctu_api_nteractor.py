from typing import Any, Dict

import httpx

from .objects import College, CourseCategory, DegreeType, Semester


class ParseException(Exception):
    pass


class NCTUAPI_Interactor:
    url: str = "https://timetable.nctu.edu.tw/"

    @staticmethod
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

    def fetch_degree_type(self, sem: Semester) -> Any:
        """Different type of courses"""
        param = {"r": "main/get_type"}
        form_data = self.get_form_data(sem)
        res = httpx.post(self.url, params=param, data=form_data)
        return res.json()

    def fetch_course_category(self, sem: Semester, deg: DegreeType) -> Any:
        param = {"r": "main/get_category"}
        form_data = self.get_form_data(sem, deg=deg)
        res = httpx.post(self.url, params=param, data=form_data)
        return res.json()

    def fetch_colleges(
        self, sem: Semester, deg: DegreeType, cat: CourseCategory
    ) -> Any:
        """Only when degree type equals to "master degree" or "undergrad"
        would have to query colleges..
        and in actual query dep api the college could leave as '*'
        """
        # TODO: we have to detect the deg type in outer loop code and not query at all
        param = {"r": "main/get_college"}
        form_data = self.get_form_data(sem, deg=deg, cat=cat)
        res = httpx.post(self.url, params=param, data=form_data)
        return res.json()

    def fetch_departments(
        self, sem: Semester, deg: DegreeType, cat: CourseCategory, col: College
    ) -> Any:
        param = {"r": "main/get_dep"}
        form_data = self.get_form_data(sem, deg=deg, cat=cat, col=col)
        res = httpx.post(self.url, params=param, data=form_data)
        return res.json()
