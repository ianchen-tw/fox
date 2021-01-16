import abc
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

JSONType = Union[str, None, Dict[str, Any], List[Any]]

class I_TargetObject(ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def fetch(self) -> Any: ...
    @abstractmethod
    def parse(self, json_data: JSONType) -> Any: ...
    @abstractmethod
    def crawl(self) -> Any: ...
    @abstractmethod
    def get_list(self) -> Any: ...
