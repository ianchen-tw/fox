from pathlib import Path
from typing import Callable

import simplejson as json
from attr import attrib, attrs


@attrs(
    auto_attribs=True,
    frozen=True,
)
class FoxCache:
    target_path: Path = attrib(converter=Path)
    encode_func: Callable = attrib(default=lambda x: x)
    decode_func: Callable = attrib(default=lambda x: x)

    def load(self):
        print(f"load from {self.target_path}")
        try:
            with open(self.target_path, "rb") as fp:
                data = json.load(fp)
                return self.decode_func(data)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def save(self, obj):
        self.target_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.target_path, "w", encoding="utf-8") as fp:
            json_data = self.encode_func(obj)
            json.dump(json_data, fp, indent="\t", ensure_ascii=False)
