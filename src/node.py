from enum import Enum, auto

class Operation(Enum):
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()

class BinOperation:
    def __init__(self, op: Operation, left: "Node", right: "Node"):
        self.left  = left 
        self.right = right
        self.operation = op
    
class FunctionDeclaration:
    def __init__(self, name: str, variables: list['Node'], body: "Node"):
        self.name = name
        self.variables = variables
        self.body = body
    
class FunctionEvaluation:
    def __init__(self, name: str, values: list["Node"], isbuiltin: bool = False):
        self.name = name
        self.values = values
        self.isbuiltin = isbuiltin

class DrawFunction:
    def __init__(self, func: str, _from: "Node", _to: "Node", step: "Node"):
        self.func = func
        self._from = _from
        self._to = _to
        self.step = step

class NodeKind(Enum):
    BINARY_OPERATION        = auto()
    INTEGER                 = auto()
    FLOAT                   = auto()
    FUNCTION_DECLARATION    = auto()
    FUNCTION_EVALUATION     = auto()
    IDENTIFIER              = auto()
    DRAW_FUNCTION           = auto()

NodeValue = int | float | BinOperation | FunctionEvaluation | FunctionDeclaration | DrawFunction

class Node:
    def __init__(self, value: NodeValue, kind: NodeKind, pos: int):
        self.value = value 
        self.kind  = kind
        self.pos   = pos