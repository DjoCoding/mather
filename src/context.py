from node import Node

class Function:
    def __init__(self, name: str, params: list[Node], body: Node):
        self.name = name
        self.params = params
        self.body = body

class Context:
    def __init__(self):
        self.functions: list[Function]= []
    
    def definefunc(self, func: Function):
        self.functions.append(func)
    
    def funcexists(self, name: str):
        for func in self.functions:
            if func.name == name:
                return True
        return False

    def findfunc(self, name: str):
        for func in self.functions:
            if func.name == name:
                return func
        return None