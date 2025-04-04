import math
from tokens import TokenKind

symbols = [
    ("+", TokenKind.PLUS),
    ("-", TokenKind.MINUS),
    ("*", TokenKind.TIMES),
    ("/", TokenKind.SLASH),
    ("(", TokenKind.PAREN_OPEN),
    (")", TokenKind.PAREN_CLOSE),
    (",", TokenKind.COMMA),
    ("=", TokenKind.EQUAL)
]

cmds = [
    ("def", TokenKind.DEF),
    ("draw", TokenKind.DRAW)
]

builtin_functions = [
    ("cos", math.cos, 1),
    ("sin", math.sin, 1),
    ("exp", math.exp, 1)
]