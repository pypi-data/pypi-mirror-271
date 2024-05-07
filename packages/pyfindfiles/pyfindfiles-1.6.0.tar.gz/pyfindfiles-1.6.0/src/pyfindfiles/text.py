from __future__ import annotations
import os
from pathlib import Path
import typing as T
from datetime import datetime
from argparse import ArgumentParser
import dateutil.parser
import shutil
import subprocess
import functools

from . import MAGENTA, BLACK

EXCLUDEDIR = ["_site", "_deps", ".git", ".eggs", "build", "dist", ".mypy_cache", ".pytest_cache"]

TXTEXT = [
    "*.py",
    "*.cfg",
    "*.ini",
    "*.txt",
    "*.md",
    "*.rst",
    "*.tex",
    "*.build",
    "*.cmake",
    "*.f",
    "*.f90",
    "*.for",
    "*.f95",
    "*.c",
    "*.h",
    "*.cpp",
    "*.cxx",
    "*.cc",
    "*.hpp",
    "*.m",
]

BINEXT = ["*.pdf"]

MAXSIZE = 10e6  # arbitrary, bytes


@functools.cache
def is_git_submodule(p: Path) -> bool:

    if not p.is_dir():
        raise NotADirectoryError("is_git_submodule() expects a directory")

    ret = subprocess.run(
        ["git", "-C", str(p), "rev-parse", "--show-superproject-working-tree"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )

    return ret.returncode == 0 and len(ret.stdout) > 0


def findtext(
    root: Path,
    txt: str,
    *,
    globext: list[str],
    exclude: list[str] | None = None,
    exclude_submod: bool = True,
    age: list[datetime] | None = None,
) -> T.Iterator[tuple[Path, dict[int, str]]]:
    """
    multiple extensions with braces like Linux does not work in .rglob()

    Parameters
    ----------
    root : pathlib.Path
        root directory to search
    txt : str
        text to search for
    globext : list[str]
        list of file extensions to search
    exclude : list[str], optional
        list of substring to exclude in path segment, by default None
    exclude_submod : bool, optional
        exclude Git submodules, by default True
    age : list[datetime], optional
        newer than date or between dates, by default None
    """

    root = Path(root).expanduser()
    if not root.is_dir():
        raise NotADirectoryError(root)

    if isinstance(globext, (str, Path)):
        globext = [str(globext)]

    exc = set(exclude) if exclude else None

    for ext in globext:
        for fn in root.rglob(ext):

            if not fn.is_file():
                continue

            finf = fn.stat()

            if finf.st_size > MAXSIZE:
                continue

            p = fn.resolve()

            # exclude substring in path segment
            if exc and exc.intersection(set(str(p).split(os.sep))):
                continue

            # exclude Git submodules
            if exclude_submod and is_git_submodule(p.parent):
                continue

            # newer than date or between dates
            if age is not None:
                mt = datetime.fromtimestamp(finf.st_mtime)
                if mt < age[0]:
                    continue
                if len(age) == 2 and mt > age[1]:
                    continue

            try:
                with p.open("r", encoding="utf8", errors="ignore") as f:
                    matches = {i: str(line) for i, line in enumerate(f) if txt in line}
            except PermissionError:
                continue

            if not matches:
                continue

            yield p, matches


def cli():
    p = ArgumentParser(description="searches for TEXT under DIR and echos back filenames")
    p.add_argument("txt", help="text to search for")  # required
    p.add_argument("globext", help="filename glob", nargs="?", default=TXTEXT)
    p.add_argument("dir", help="root dir to search", nargs="?", default=".")
    p.add_argument("-t", "--time", help="newer than date or between dates", nargs="+")
    p.add_argument("-c", "--run", help="command to run on files e.g. notepad++")
    p.add_argument("-e", "--exclude", help="exclude files/dirs", nargs="+", default=EXCLUDEDIR)
    p.add_argument("-x", "--exclude_submod", action="store_true", default=True)
    p.add_argument("-v", "--verbose", action="store_true")
    P = p.parse_args()

    # %% preflight
    root = Path(P.dir).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"{root} is not a directory.")

    if P.run:
        exe = shutil.which(P.run)  # necessary for some Windows program e.g. VScode
        if not exe:
            raise SystemExit(f"could not find {exe}")

    time = None
    if P.time:
        time = [dateutil.parser.parse(t) for t in P.time]
    # %% main
    for fn, matches in findtext(
        P.dir,
        P.txt,
        globext=P.globext,
        exclude=P.exclude,
        exclude_submod=P.exclude_submod,
        age=time,
    ):
        if P.verbose:
            print(MAGENTA + str(fn) + BLACK)
            for k, v in matches.items():
                print(k, ":", v)
        else:
            print(fn)

        if P.run:
            subprocess.run([exe, str(fn)])


if __name__ == "__main__":
    cli()
