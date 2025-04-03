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
    def __init__(self, name: str, values: list["Node"]):
        self.name = name
        self.values = values

class NodeKind(Enum):
    BINARY_OPERATION        = auto()
    INTEGER                 = auto()
    FLOAT                   = auto()
    FUNCTION_DECLARATION    = auto()
    FUNCTION_EVALUATION     = auto()
    IDENTIFIER              = auto()

NodeValue = int | float | BinOperation | FunctionEvaluation | FunctionDeclaration

class Node:
    def __init__(self, value: NodeValue, kind: NodeKind, pos: int):
        self.value = value 
        self.kind  = kind
        self.pos   = pos