from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

JSONType = Union[str, None, Dict[str, Any], List[Any]]


class I_TargetObject(ABC):
    @abstractmethod
    def fetch(self):
        pass

    @abstractmethod
    def parse(self, json_data: JSONType):
        pass

    @abstractmethod
    def crawl(self):
        pass

    @abstractmethod
    def get_list(self):
        pass
