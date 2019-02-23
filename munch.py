#!/usr/bin/env python3
"""token-muncher — small lexer for a C-like expression language."""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from typing import Iterator, List, Optional

TOKEN_SPEC = [
    ("COMMENT", r"//[^\n]*|/\*.*?\*/"),
    ("NUMBER", r"\d+(?:\.\d+)?"),
    ("ID", r"[A-Za-z_][A-Za-z0-9_]*"),
    ("STRING", r'"(?:\\.|[^"\\])*"'),
    ("CHAR", r"'(?:\\.|[^'\\])'"),
    ("OP", r"==|!=|<=|>=|&&|\|\||[+\-*/%=<>!&|^~]"),
    ("PUNCT", r"[(){}\[\];,.]"),
    ("WS", r"[ \t\r\n]+"),
    ("MISMATCH", r"."),
]

MASTER = re.compile("|".join(f"(?P<{n}>{p})" for n, p in TOKEN_SPEC), re.S)

KEYWORDS = {
    "if", "else", "while", "for", "return", "int", "float", "char",
    "void", "true", "false", "null",
}


@dataclass(frozen=True)
class Token:
    kind: str
    value: str
    line: int
    col: int

    def __str__(self) -> str:
        return f"{self.kind:<8} {self.value!r:>16}  @ {self.line}:{self.col}"


def tokenize(src: str) -> Iterator[Token]:
    line = 1
    col = 1
    for m in MASTER.finditer(src):
        kind = m.lastgroup or "MISMATCH"
        value = m.group()
        start = m.start()
        # track line/col from start of match
        before = src[:start]
        line = before.count("\n") + 1
        last_nl = before.rfind("\n")
        col = start - last_nl

        if kind == "WS":
            continue
        if kind == "COMMENT":
            continue
        if kind == "MISMATCH":
            raise SyntaxError(f"unexpected {value!r} at {line}:{col}")
        if kind == "ID" and value in KEYWORDS:
            kind = "KEYWORD"
        yield Token(kind, value, line, col)


def tokenize_all(src: str) -> List[Token]:
    return list(tokenize(src))


def main(argv: Optional[List[str]] = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        print("usage: munch.py '<source>' | munch.py -f file.c", file=sys.stderr)
        return 2
    if argv[0] == "-f":
        with open(argv[1], encoding="utf-8") as fh:
            src = fh.read()
    else:
        src = " ".join(argv)
    try:
        for tok in tokenize(src):
            print(tok)
    except SyntaxError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
