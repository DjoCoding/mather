from node import Node
from dataclasses import dataclass

@dataclass
class ParserExceptionOptions:
    message: str
    node: Node

class ParserException(Exception):
    def __init__(self, options: ParserExceptionOptions):
        super().__init__(options.message)
        self.node = options.node
    
    def format(self):
        return f"{'end' if self.node.pos == -1 else self.node.pos}: {str(self)}"
