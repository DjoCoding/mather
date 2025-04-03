from tokens import Token, TokenKind
from symbols import symbols
from errors.lexer import LexerException, LexerExceptionOptions
from checker import Checker, NumberType

class Lexer:
    def __init__(self, content: str):
        self.content = content
        self.current = 0
    
    def __peek(self):
        return self.content[self.current]
    

    def __consume(self):
        self.current += 1

    def __end(self):
        return self.current >= len(self.content)

    def __pos(self):
        return self.current + 1

    def __pos_and_move(self):
        pos = self.__pos()
        self.__consume()
        return pos

    def __get_token(self):
        c = self.__peek()
        
        for value, kind in symbols:
            if c == value:
                return Token(kind, value, self.__pos_and_move())
        
        if not c.isdigit():
            current = self.current
            v = ""

            while not self.__end():
                c = self.__peek()
                if not c.isalpha():
                    break
                v += c
                self.__consume()
            
            return Token(TokenKind.IDENTIFIER if v != "def" else TokenKind.DEF, v, current)

        number = ""
        current = self.current

        while not self.__end():
            c = self.__peek()
            
            if not c.isdigit():
                if c != ".":
                    break
                number += c
                self.__consume()
                continue
            
            number += c
            self.__consume()
        
        type = Checker.checkIfValidNumber(number)
        if type == NumberType.NAN:
            raise LexerException(LexerExceptionOptions(current, f"Invalid number found `{number}`"))
    
        return Token(TokenKind.FLOAT if type == NumberType.FLOAT else TokenKind.INTEGER, number, current)

    def lex(self) -> tuple[list[Token] | None, LexerException | None]:
        tokens: list[Token] = []
        
        while not self.__end():
            if self.__peek().isspace():
                self.__consume()
                continue

            try:
                token = self.__get_token()
            except LexerException as e:
                return None, e

            tokens.append(token)

        tokens.append(Token(TokenKind.END, "", -1))
        return tokens, None

