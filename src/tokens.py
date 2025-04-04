from enum import Enum, auto

class TokenKind(Enum):
    PLUS            = auto()
    MINUS           = auto()
    TIMES           = auto()
    SLASH           = auto()
    PAREN_OPEN      = auto()
    PAREN_CLOSE     = auto()
    INTEGER         = auto()
    FLOAT           = auto()
    IDENTIFIER      = auto()
    DEF             = auto()
    EQUAL           = auto()
    COMMA           = auto()
    DRAW            = auto()
    END             = auto()

    def __str__(self):
        if self == TokenKind.PLUS:
            return "PLUS"
        if self == TokenKind.MINUS:
            return "MINUS"
        if self == TokenKind.TIMES:
            return "TIMES"
        if self == TokenKind.SLASH:
            return "SLASH"
        if self == TokenKind.PAREN_OPEN:
            return "PAREN_OPEN"
        if self == TokenKind.PAREN_CLOSE:
            return "PAREN_CLOSE"
        if self == TokenKind.INTEGER:
            return "INTEGER"
        if self == TokenKind.FLOAT:
            return "FLOAT"
        if self == TokenKind.IDENTIFIER:
            return "IDENTIFIER"
        if self == TokenKind.DEF:
            return "DEF"
        if self == TokenKind.EQUAL:
            return "EQUAL"
        if self == TokenKind.END:
            return "END"
        if self == TokenKind.COMMA:
            return "COMMA"
        if self == TokenKind.DRAW:
            return "DRAW"
        return "None"

class Token:
    def __init__(self, kind: TokenKind, value: str, pos: int):
        self.kind = kind
        self.value = value
        self.pos = pos
    
    def __str__(self):
        return f"{self.pos}: {self.kind} - `{self.value}`"