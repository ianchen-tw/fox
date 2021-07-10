import argparse
from typing import TYPE_CHECKING, Literal

import rich
from pydantic import BaseModel

if TYPE_CHECKING:
    from dataclasses import dataclass
else:

    def dataclass(model):
        return model


@dataclass
class TypedArgs(BaseModel):
    year: int
    term: Literal["1", "2", "x"]

    @classmethod
    def from_arg_parse(self, args: argparse.Namespace):
        pass


def main():
    parser = argparse.ArgumentParser(description="fox: your tool", epilog="Enjoy!")
    parser.add_argument("--year", help="academic year")
    parser.add_argument("--term", help="term")
    args = parser.parse_args()
    rich.print(args)

    # li = Literal["1", "2", "x"]
    # print(f"literal: {li}")
    # args = TypedArgs()
    # rich.print(li)


if __name__ == "__main__":
    main()
