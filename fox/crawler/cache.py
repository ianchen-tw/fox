import json
from pathlib import Path
from typing import Dict, List, Optional

from .target_object.meta_object import Course, Department, Semester
from .types import JSONType


class Cache:
    @staticmethod
    def get_path() -> Path:
        return Path("./Cache/")

    @staticmethod
    def dep_dump(sem: Semester, deps=Optional[List[Department]]):
        path = Cache.get_path() / str(sem) / "dep_uuid_list.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as fp:
            json_data = [dep.__dict__ for dep in deps]
            json.dump(json_data, fp, indent="\t", ensure_ascii=False)

    @staticmethod
    def dep_load(sem: Semester) -> List[Department]:
        path = Cache.get_path() / str(sem) / "dep_uuid_list.json"
        try:
            with open(path, "rb") as fp:
                data: List[Dict[str, str]] = json.load(fp)
                return [Department(**d) for d in data]
        except FileNotFoundError:
            return []

    @staticmethod
    def course_dump(sem: Semester, dep: Department, courses=Optional[List[Course]]):
        path = Cache.get_path() / str(sem) / "course" / f"{str(dep)}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as fp:
            json_data = [course.__dict__ for course in courses]
            json.dump(json_data, fp, indent="\t", ensure_ascii=False)

    @staticmethod
    def course_load(sem: Semester, dep: Department) -> List[Course]:
        path = Cache.get_path() / str(sem) / "course" / f"{str(dep)}.json"
        try:
            with open(path, "rb") as fp:
                data: JSONType = json.load(fp)
                assert isinstance(data, list)
                return [Course(**d) for d in data]
        except FileNotFoundError:
            return []
