"""Markdown Table Linter, lint your markdown tables with CJK letters."""

import argparse
import os
import re
from datetime import date
from io import StringIO
from typing import Iterable, TextIO

name = "Markdown Table Linter"
desc = "Lint markdown tables with CJK characters."
author = "Philip Fan"
version = "1.0.0"


def main():
    parser = argparse.ArgumentParser(
        prog=name, description=desc, epilog=f"Apache-2.0 {date.today().year}©{author}."
    )

    parser.add_argument("dirname")
    parser.add_argument("--cjk", default=1.83)
    parser.add_argument("-v", "--version", action="store_true")

    args = parser.parse_args()

    if args.version:
        print(f"{name} version {version}")
        exit()


    def walk_files(
        dirname: str | None = None, pattern: re.Pattern | None = None
    ) -> Iterable[str]:
        """Walk through all files under the directory."""
        if dirname is None:
            dirname = os.getcwd()
        else:
            dirname = os.path.abspath(dirname)
        for foldername, _, filenames in os.walk(dirname):
            for filename in filenames:
                if pattern and not pattern.fullmatch(filename):
                    continue
                yield os.path.join(foldername, filename)


    def compute_length(string: str) -> float:
        """Compute the length of a string"""
        length = 0
        for char in string:
            if ord(char) < 256:
                length += 1
            else:
                length += float(args.cjk)
        return length


    def nearest_int(number: float) -> int:
        """Find the nearest integer to the number."""
        return int(number + 0.5)


    def lint_table(rows: list[str]) -> Iterable[str]:
        """Lint the table."""
        pat = re.compile(r"(?<!\\)\|")
        splited = [[item.strip() for item in pat.split(row)][1:-1] for row in rows]
        lengths = [[compute_length(item) for item in row] for row in splited]
        column = max(len(row) for row in lengths)

        for row in lengths:
            row += [0] * (column - len(row))

        maxes = [
            max(row[i] for j, row in enumerate(lengths) if j != 1) + 2
            for i in range(column)
        ]
        poses = [sum(maxes[: i + 1]) for i in range(column)]

        for i, row in enumerate(splited):
            linted = []
            total_length = 0

            if i == 1:
                for j, item in enumerate(row):
                    length = nearest_int(poses[j] - total_length)
                    linted.append("-" * length)
                    total_length += length

                    if item.startswith(":"):
                        linted[-1] = ":" + linted[-1][1:]
                    if item.endswith(":"):
                        linted[-1] = linted[-1][:-1] + ":"

            else:
                for j, item in enumerate(row):
                    length = nearest_int(poses[j] - total_length - compute_length(item))
                    linted.append(" " + item + " " * (length - 1))
                    total_length += compute_length(item) + length

            yield "|" + "|".join(linted) + "|"


    def lint_file(stream: TextIO) -> str:
        compiled = StringIO()
        table = []
        pat = re.compile(r"\s*\|(.*?\|)+\s*")

        for line in stream:
            if line.endswith("\n"):
                line = line[:-1]
            if pat.fullmatch(line):
                table.append(line)
            else:
                if table:
                    for row in lint_table(table):
                        compiled.write(row + "\n")
                    table = []
                compiled.write(line + "\n")

        compiled.seek(0)
        return compiled.read()


    pat = re.compile(r".*\.mdx?")

    for filename in walk_files("src", pat):
        with open(filename, "r") as stream:
            compiled = lint_file(stream)
        with open(filename, "w") as stream:
            stream.write(compiled)


if __name__ == '__main__':
    main()
