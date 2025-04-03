from evaluator import Result
from enum import Enum, auto
from dataclasses import dataclass

class ResultKind(Enum):
    VALID = auto()
    ERROR = auto()

ResultValue = int | float | str

@dataclass
class HistoryResult:
    kind: ResultKind
    v: ResultValue

class History:
    def __init__(self):
        self.history: list[(str, HistoryResult)] = []
        self.current = 0

    def push(self, s: str, v: HistoryResult):
        self.history.append((s, v))
        self.current = len(self.history)
    
    def up(self) -> tuple[str, HistoryResult | None]:
        if self.current != 0:
            self.current -= 1
            return self.history[self.current]
        
        if len(self.history) == 0:
            return "", None
        
        return self.history[0]

    def down(self) -> tuple[str, HistoryResult | None]:
        if self.current == len(self.history):
            return "", None
        
        s, v = self.history[self.current]
        self.current += 1
        
        return s, v


