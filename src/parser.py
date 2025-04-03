from tokens import Token, TokenKind
from node import Node, BinOperation, Operation, NodeKind, FunctionDeclaration, FunctionEvaluation
from tree import AST
from basic_parser import BasicParser
from errors.parser import ParserException, ParserExceptionOptions

ASTorException  = tuple[AST | None, ParserException | None]
NodeOrException = tuple[Node | None, ParserException | None]

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens  = tokens
        self.current = 0

    def __peek(self):
        return self.tokens[self.current]

    def __consume(self):
        token = self.tokens[self.current]
        self.current += 1
        return token

    def __end(self):
        return self.__peek().kind == TokenKind.END

    def __parse_function_variables(self) -> tuple[list[Node] | None, ParserException | None]:
        if self.__peek().kind != TokenKind.PAREN_OPEN:
            return None, ParserException(ParserExceptionOptions(f"Expected a `(` but token of kind `{str(self.__peek().kind)}` found", self.__peek()))
        self.__consume()

        variables = []
        ids = dict()

        if self.__peek().kind == TokenKind.PAREN_CLOSE:
            self.__consume()
            return variables, None
        

        while True:
            if self.__peek().kind != TokenKind.IDENTIFIER:
                return None, ParserException(ParserExceptionOptions(f"Expected an identifier but token of kind `{str(self.__peek().kind)}` found", self.__peek()))

            var = self.__peek().value
            variables.append(Node(var, NodeKind.IDENTIFIER, self.__peek().pos))

            if ids.get(var) != None:
                return None,  ParserException(ParserExceptionOptions(f"more of just one parameter `{var}` found")) 

            ids.setdefault(var, 1)

            self.__consume()

            if self.__peek().kind == TokenKind.COMMA:
                self.__consume()
                continue
            
            if self.__peek().kind == TokenKind.PAREN_CLOSE:
                break
            
            return None, ParserException(ParserExceptionOptions(f"Expected ')' but token of kind `{str(self.__peek().kind)}` found", self.__peek()))

        if self.__peek().kind != TokenKind.PAREN_CLOSE:
            return None, ParserException(ParserExceptionOptions(f"Expected a `(` but token of kind `{str(self.__peek().kind)}` found", self.__peek()))
        self.__consume()

        return variables, None

    def __parse_function_declaration(self) -> NodeOrException:
        if self.__peek().kind != TokenKind.DEF:
            return None, ParserException(ParserExceptionOptions(f"Expected a function declaration but token of kind `{str(self.__peek().kind)}` found", self.__peek()))
        pos = self.__peek().pos
        self.__consume()

        if self.__peek().kind != TokenKind.IDENTIFIER:
            return None, ParserException(ParserExceptionOptions(f"Expected a function name but token of kind `{str(self.__peek().kind)}` found", self.__peek()))

        name = self.__peek().value
        self.__consume()

        variables, err = self.__parse_function_variables()
        if err:
            return None, err

        if self.__peek().kind != TokenKind.EQUAL:
            return None, ParserException(ParserExceptionOptions(f"Expected a `=` but token of kind `{str(self.__peek().kind)}` found", self.__peek()))
        self.__consume()

        body, err = self.__parse_addition()
        if err:
            return None, err
    
        return Node(FunctionDeclaration(name, variables, body), NodeKind.FUNCTION_DECLARATION, pos), None

    def __parse_function_values(self) -> tuple[list[Node] | None, ParserException | None]:
        if self.__peek().kind != TokenKind.PAREN_OPEN:
            return None, ParserException(ParserExceptionOptions(f"Expected `(` but token of kind `{str(self.__peek().kind)}` found", self.__peek()))
        self.__consume()

        values: list[Node] = []

        if self.__peek().kind == TokenKind.PAREN_CLOSE:
            self.__consume()
            return values, None

        while True:
            value, err = self.__parse_addition()
            if err:
                return None, err
            
            values.append(value)

            if self.__peek().kind == TokenKind.COMMA:
                self.__consume()
                continue
            
            if self.__peek().kind == TokenKind.PAREN_CLOSE:
                break
            
            return None, ParserException(ParserExceptionOptions(f"Expected ')' but token of kind `{str(self.__peek().kind)}` found", self.__peek()))

        if self.__peek().kind != TokenKind.PAREN_CLOSE:
            return None, ParserException(ParserExceptionOptions(f"Expected a `(` but token of kind `{str(self.__peek().kind)}` found", self.__peek()))
        self.__consume()

        return values, None
        


    def __parse_function_evaluation(self) -> NodeOrException:
        if self.__peek().kind != TokenKind.IDENTIFIER:
            return None, ParserException(ParserExceptionOptions(f"Expected an identifier but token of kind `{str(self.__peek().kind)}` found", self.__peek()))

        name = self.__peek().value
        pos = self.__peek().pos
        self.__consume()

        values, err = self.__parse_function_values()
        if err:
            return None, err

        return Node(FunctionEvaluation(name, values), NodeKind.FUNCTION_EVALUATION, pos), None

    def __parse_primary(self) -> NodeOrException:
        token = self.__peek()
        
        if token.kind == TokenKind.INTEGER:
            self.__consume()
            return Node(BasicParser.parse_int(token.value), NodeKind.INTEGER, token.pos), None

        if token.kind == TokenKind.FLOAT:
            self.__consume()
            return Node(BasicParser.parse_float(token.value), NodeKind.FLOAT, token.pos), None
        
        if token.kind == TokenKind.PAREN_OPEN:
            self.__consume()
            v, err = self.__parse_addition()
            
            if err:
                return None, err

            if self.__peek().kind != TokenKind.PAREN_CLOSE:
                return None, ParserException(ParserExceptionOptions(f"Expected token `)` but found token of kind `{str(self.__peek().kind)}`", self.__peek()))

            self.__consume()
            return v, None
    
        if token.kind == TokenKind.IDENTIFIER:
            after = self.tokens[self.current + 1]
            if after.kind == TokenKind.PAREN_OPEN:
                return self.__parse_function_evaluation()
            
            pos = self.__peek().pos
            self.__consume()
            return Node(token.value, NodeKind.IDENTIFIER, pos), None
        
        return None, ParserException(ParserExceptionOptions(f"Unexpected token of kind `{str(self.__peek().kind)}` found", self.__peek()))

    def __parse_multiplication(self) -> NodeOrException:
        left, err = self.__parse_primary()
        if err:
            return None, err
        
        while not self.__end():
            tok = self.__peek()
            
            if tok.kind != TokenKind.TIMES and tok.kind != TokenKind.SLASH:
                break
            
            pos = tok.pos
            op = Operation.MUL if tok.kind == TokenKind.TIMES else Operation.DIV
            self.__consume()

            right, err = self.__parse_multiplication()
            if err:
                return None, err
            
            binop = BinOperation(op, left, right)
            left = Node(binop, NodeKind.BINARY_OPERATION, pos)
        
        return left, None


    def __parse_addition(self) -> NodeOrException:
        left, err = self.__parse_multiplication()
        if err:
            return None, err
        
        while not self.__end():
            tok = self.__peek()
            
            if tok.kind != TokenKind.PLUS and tok.kind != TokenKind.MINUS:
                break
            
            pos = tok.pos
            op = Operation.ADD if tok.kind == TokenKind.PLUS else Operation.SUB
            self.__consume()

            right, err = self.__parse_addition()
            if err:
                return None, err
            
            binop = BinOperation(op, left, right)
            left = Node(binop, NodeKind.BINARY_OPERATION, pos)
        
        return left, None

    def __parse_expression(self):
        if self.__peek().kind != TokenKind.DEF:
            return self.__parse_addition()

        return self.__parse_function_declaration()

    def parse(self) -> ASTorException:
        root, err = self.__parse_expression()
        
        if err:
            return None, err
        
        ast = AST(root)
        return ast, None
