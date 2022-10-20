import sys
from typing import Any, Tuple

TITLE = "\33[92;1m"
SUBTITLE = "\33[94m"
INFO = ""
WARN = "\33[93m"
ERROR = "\33[91m"
CLEAR = "\33[0m"

ITALIC = "\33[3;36m"
LINE = "\33[90m"


def italic_args(args: Tuple[Any], col: str) -> Tuple[str]:
    """Add italic style to all arguments"""
    return tuple([f"{ITALIC}{arg}{col}" for arg in args])


def title(text: str, *args: Any) -> None:
    """Print title"""
    print(f"{TITLE}{text}{CLEAR}" % italic_args(args, TITLE))


def subtitle(text: str, *args: Any) -> None:
    """Print subtitle"""
    print(f"{SUBTITLE}{text}{CLEAR}" % italic_args(args, SUBTITLE))


def info(text: str, *args: Any) -> None:
    """Print info"""
    print(f"{INFO}{text}{CLEAR}" % italic_args(args, INFO))


def warn(text: str, *args: Any) -> None:
    """Print warning"""
    print(f"{WARN}{text}{CLEAR}" % italic_args(args, WARN))


def error(text: str, *args: Any) -> None:
    """Print error"""
    print(f"{ERROR}{text}{CLEAR}" % italic_args(args, ERROR))


def fatal(text: str, *args: Any) -> None:
    """Print error and exit"""
    sys.exit(f"{ERROR}{text}{CLEAR}" % italic_args(args, ERROR))


def inpt(text: str, *args: Any) -> str:
    """Get user input"""
    return input(text % italic_args(args, CLEAR))
