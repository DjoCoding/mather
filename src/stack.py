from typing import cast
StackQueryType = int | float | None

class Stack:
    def __init__(self):
        self.__stack: list[dict] = []
    
    def push(self, func: str, map: dict):
        v = dict()
        v["func"] = func
        v["values"] = map
        self.__stack.append(v)
    
    def pop(self):
        return self.__stack.pop()

    def consult(self):
        return self.__stack[len(self.__stack) - 1]

    def end(self):
        return len(self.__stack) == 0

    def findtop(self, id: str) -> StackQueryType:
        if self.end():
            return None
        
        return cast(dict, self.consult()["values"]).get(id)