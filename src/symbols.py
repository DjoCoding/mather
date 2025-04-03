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