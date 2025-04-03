from dataclasses import dataclass

@dataclass
class LexerExceptionOptions:
    position: int
    message: str


class LexerException(Exception):
    def __init__(self, options: LexerExceptionOptions):
        super().__init__(options.message)
        self.position = options.position
    
    def format(self):
        return f"{self.position}: {str(self)}"
