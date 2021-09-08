from typing import List, Optional

from fox.api.form_types import Department
from fox.types import Semester
from .dep_108_1 import data as data_1081
from .dep_108_2 import data as data_1082
from .dep_108_X import data as data_108X
from .dep_109_1 import data as data_1091
from .dep_109_2 import data as data_1092
from .dep_109_X import data as data_109X
from .dep_110_1 import data as data_1101

# only cache for 3 year
cached_deps = {
    "1081": data_1081,
    "1082": data_1082,
    "108X": data_108X,
    "1091": data_1091,
    "1092": data_1092,
    "109X": data_109X,
    "1101": data_1101,
}


def cache_get_deps(sem: Semester) -> Optional[List[Department]]:
    s = f"{sem}"
    if s not in cached_deps:
        return None
    deps = [Department(**dic) for dic in cached_deps[s]]
    return deps


__all__ = ["cached_deps", "cache_get_deps"]
