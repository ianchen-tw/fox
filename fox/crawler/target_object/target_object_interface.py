from typing import Any, Dict, List, Union

from typing_extensions import Protocol

JSONType = Union[str, None, Dict[str, Any], List[Any]]


class CrawlTarget(Protocol):
    def fetch(self):
        raise NotImplementedError

    def parse(self, json_data: JSONType):
        raise NotImplementedError

    def crawl(self):
        raise NotImplementedError

    def get_list(self):
        raise NotImplementedError
