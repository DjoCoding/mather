from tokens import Token
from dataclasses import dataclass

@dataclass
class ParserExceptionOptions:
    message: str
    token: Token

class ParserException(Exception):
    def __init__(self, options: ParserExceptionOptions):
        super().__init__(options.message)
        self.token = options.token
    
    def format(self):
        return f"{'end' if self.token.pos == -1 else self.token.pos}: {str(self)}"
