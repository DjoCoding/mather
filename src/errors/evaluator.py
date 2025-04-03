from tree import Node
from dataclasses import dataclass

@dataclass
class EvaluatorExceptionOptions:
    node: Node
    message: str


class EvaluatorException(Exception):
    def __init__(self, options: EvaluatorExceptionOptions):
        super().__init__(options.message)
        self.node = options.node

    def format(self):
        return f"{self.node.pos}: {str(self)}"
    
