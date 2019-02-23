#!/usr/bin/env python3
import unittest
from munch import tokenize_all


class TestLexer(unittest.TestCase):
    def test_assignment(self):
        toks = tokenize_all("sum = a + 42;")
        kinds = [t.kind for t in toks]
        self.assertEqual(kinds, ["ID", "OP", "ID", "OP", "NUMBER", "PUNCT"])

    def test_keywords(self):
        toks = tokenize_all("if (true) return 1;")
        self.assertEqual(toks[0].kind, "KEYWORD")
        self.assertEqual(toks[0].value, "if")

    def test_string(self):
        toks = tokenize_all('msg = "hi";')
        self.assertEqual(toks[2].kind, "STRING")

    def test_comment_skipped(self):
        toks = tokenize_all("x // comment\n+ 1")
        self.assertEqual([t.value for t in toks], ["x", "+", "1"])


if __name__ == "__main__":
    unittest.main()
