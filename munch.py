#!/usr/bin/env python3
"""token-muncher — tiny lexer for compiler-design practice."""
from __future__ import print_function
import re, sys

SPEC = [
    ("NUMBER", r"\d+"),
    ("ID", r"[A-Za-z_]\w*"),
    ("OP", r"==|!=|<=|>=|[+\-*/=<>]"),
    ("PUNCT", r"[;(),{}]"),
    ("SKIP", r"[ \t\n]+"),
    ("MISMATCH", r"."),
]
MASTER = re.compile("|".join("(?P<%s>%s)" % p for p in SPEC))

def tokenize(text):
    for m in MASTER.finditer(text):
        kind = m.lastgroup
        val = m.group()
        if kind == "SKIP":
            continue
        if kind == "MISMATCH":
            raise ValueError("unexpected %r" % val)
        yield kind, val

def main():
    src = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "x = 10 + y;"
    print("source:", src)
    for kind, val in tokenize(src):
        print("%-8s %r" % (kind, val))

if __name__ == "__main__":
    main()
