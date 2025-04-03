from lexer import Lexer
from tokens import Token 
from errors.lexer import LexerException

from parser import Parser
from tree import AST
from errors.parser import ParserException


from evaluator import Evaluator, Result
from errors.evaluator import EvaluatorException

from context import Context

from history import History, HistoryResult, ResultKind

context = Context()

def get_result(num: float | int | str):
    if isinstance(num, int):
        return num 
    
    if isinstance(num, str):
        return num
    
    if num.is_integer():
        return int(num)
    
    return num


def lexorraise(content: str) -> list[Token]:
    lexer = Lexer(content)
    tokens, err = lexer.lex()
    
    if err:
        raise err
    
    return tokens

def parseorraise(tokens: list[Token]) -> AST:
    parser = Parser(tokens)
    ast, err = parser.parse()
    
    if err:
        raise err
    
    return ast

def evaluateorraise(tree: AST) -> Result:
    evaluator = Evaluator(tree, context)
    result, err = evaluator.eval()

    if err:
        raise err
    
    return get_result(result)

def run():
    content = ""
    history = History()

    while True: 
        content = input("> ")
        if content.lower() == "q" or content.lower() == "quit":
            break

        c = content.strip().lower()
        if c == "":
            continue

        if c == "u":
            prompt, r = history.up()

            if r == None:
                print()
            else:
                print(f"{prompt} -> {get_result(r.v) if r.kind == ResultKind.VALID else r.v}")

            continue
        
        if c == "d":
            prompt, r = history.down()
            
            if r == None:
                print()
            else:                
                print(f"{prompt} -> {get_result(r.v) if r.kind == ResultKind.VALID else r.v}")
            
            continue
            

        tokens = []
        try:
            tokens = lexorraise(content)
        except LexerException as e:
            err = e.format()
            history.push(content, HistoryResult(ResultKind.ERROR, err))
            print(err)
            continue

        ast: AST | None = None
        try:
            ast = parseorraise(tokens)
        except ParserException as e:
            err = e.format()
            history.push(content, HistoryResult(ResultKind.ERROR, err))
            print(err)
            continue
        
        result: Result = 0
        try:
            result = evaluateorraise(ast)
        except EvaluatorException as e:
            err = e.format()
            history.push(content, HistoryResult(ResultKind.ERROR, err))
            print(err)
            continue
    
        history.push(content, HistoryResult(ResultKind.VALID, result))
        print(result)
    

def main():
    run()
    exit(0)

if __name__ == "__main__":
    main()
