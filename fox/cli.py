import argparse
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, validator
from pydantic.error_wrappers import ValidationError
from rich.console import Console
from rich.table import Table
from rich.text import Text

from fox.api.dep import DepManager
from fox.config import Config
from fox.types import Semester

if TYPE_CHECKING:
    from dataclasses import dataclass
else:

    def dataclass(model):
        return model


@dataclass
class TypedArgs(BaseModel):
    year: int
    term: str
    gen_dep_cache: bool

    @validator("term")
    def term_must_be_in_range(cls, val):
        accepted_values = ["1", "2", "X"]
        if val not in accepted_values:
            msg = Text(
                f"Must be one of [yellow]{accepted_values}[/yellow], get: [red]{val}[/red]"
            )
            raise ValueError(msg)
        return str(val)

    @classmethod
    def from_parsed_args(cls, args) -> Optional["TypedArgs"]:
        try:
            instance = cls(
                gen_dep_cache=args.gen_dep_cache, year=args.year, term=args.term
            )
            return instance
        except ValidationError as e:
            explain_validation_error(e)
        return None


def explain_validation_error(e: ValidationError):
    table = Table(padding=1, pad_edge=True)
    table.title = "[red]Arguemnt failed"
    table.add_column("Argument", justify="center", style="bold red")
    table.add_column("Description")
    for err in e.errors():
        table.add_row(err["loc"][0], err["msg"])
    console = Console(
        force_terminal=True,
    )
    console.print(table)


def main():
    parser = argparse.ArgumentParser(prog="fox")
    parser.add_argument("year", help="academic year")
    parser.add_argument("term", help="term: [1|2|X]")
    parser.add_argument(
        "--gen-dep-cache",
        action="store_true",
        help="generate department cache (only for lib development)",
    )

    args = TypedArgs.from_parsed_args(parser.parse_args())
    if args is None:
        parser.print_help()
        return -1

    config = Config()
    if args.gen_dep_cache is True:
        config.save_dep_result = True

    sem = Semester(year=args.year, term=args.term)

    dep_manager = DepManager(sem)
    dep_manager.run()
    dep_manager.get_deps()
    if config.save_dep_result is True:
        dep_manager.condense()


if __name__ == "__main__":
    main()
