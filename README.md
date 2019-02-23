# Token Muncher

Small lexer for a C-like expression language. Emits tokens for identifiers, keywords, numbers, operators, punctuation, and string literals. Comments and whitespace are skipped.

## Run

```bash
python3 munch.py 'sum = a + 42;'
python3 munch.py -f sample.c
python3 -m unittest test_munch.py -v
```

## Example

```text
$ python3 munch.py 'if (n >= 10) return "ok";'
KEYWORD  'if'             @ 1:1
PUNCT    '('              @ 1:4
ID       'n'              @ 1:5
OP       '>='             @ 1:7
NUMBER   '10'             @ 1:10
PUNCT    ')'              @ 1:12
KEYWORD  'return'         @ 1:14
STRING   '"ok"'           @ 1:21
PUNCT    ';'              @ 1:25
```

## Scope

This is a scanner only — no parser or AST. Useful as a compiler-design exercise and as a building block for a recursive-descent parser later.

## License

MIT
