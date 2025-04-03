from enum import Enum, auto

class NumberType(Enum):
    INTEGER = auto()
    FLOAT   = auto()
    NAN     = auto()

class Checker():
    @staticmethod
    def checkIfValidNumber(strnum: str) -> NumberType:
        isfloat = False

        for i, c in enumerate(strnum):
            if c.isdigit():
                continue

            if i == 0:
                return NumberType.NAN
            
            if c == "." and isfloat:
                return NumberType.NAN
            
            isfloat = True
        
        return NumberType.FLOAT if isfloat else NumberType.INTEGER
        
            
                
                    
    