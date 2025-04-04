from stack import Stack
from tree import AST
from node import Node, NodeKind, BinOperation, Operation, DrawFunction, FunctionDeclaration, FunctionEvaluation
from errors.evaluator import EvaluatorException, EvaluatorExceptionOptions
from context import Context, Function
from drawer import Drawer, DrawerInput
from symbols import builtin_functions
from typing import cast

Result = int | float | DrawerInput
ResultOrError = tuple[Result | None, EvaluatorException | None]

class Evaluator:
    def __init__(self, tree: AST, context: Context):
        self.tree = tree         # ast
        self.context = context   # for global function definitions 
        self.stack = Stack()     # for function execution
    
    def __evaluate_on_values(self, node: Node, op: Operation, left: Result, right: Result) -> ResultOrError:
        if op == Operation.ADD:
            return left + right, None

        if op == Operation.SUB:
            return left - right, None

        if op == Operation.MUL:
            return left * right, None

        if op == Operation.DIV:
            if right == 0:
                return None, EvaluatorException(EvaluatorExceptionOptions(node, f"Division by zero is undefined"))       
            return left / right, None
        
        raise NotImplementedError()
    
    def __evaluate_identifier(self, node: Node) -> ResultOrError:
        id = cast(str, node.value)

        value = self.stack.findtop(id)
        if value == None:
            return None, EvaluatorException(EvaluatorExceptionOptions(node, f"No value found for identifier {id}"))

        return value, None


    def __evaluate_node_with_map(self, node: Node) -> ResultOrError:
        if node.kind == NodeKind.INTEGER:
            return self.__evaluate_int(node)
        
        if node.kind == NodeKind.FLOAT:
            return self.__evaluate_float(node)

        if node.kind == NodeKind.IDENTIFIER:
            return self.__evaluate_identifier(node)
    
        if node.kind == NodeKind.FUNCTION_EVALUATION:
            return self.__evaluate_function_eval(node)
    
        if node.kind == NodeKind.BINARY_OPERATION:
            binop = cast(BinOperation, node.value)

            left, err = self.__evaluate_node_with_map(binop.left)
            if err:
                return None, err
            
            right, err = self.__evaluate_node_with_map(binop.right)
            if err:
                return None, err

            return self.__evaluate_on_values(node, binop.operation, left, right)
    
        raise NotImplementedError()
        
    def __evaluate_binop(self, node: Node) -> ResultOrError:
        binop = cast(BinOperation, node.value)

        left, err = self.__evaluate_node(binop.left)
        if err:
            return None, err

        right, err = self.__evaluate_node(binop.right)
        if err:
            return None, err

        return self.__evaluate_on_values(node, binop.operation, left, right)
    
    def __evaluate_float(self, node: Node) -> ResultOrError:
        f = cast(float, node.value)
        return f, None

    def __evaluate_int(self, node: Node) -> ResultOrError:
        i = cast(int, node.value)
        return i, None

    def __evaluate_builtin_function(self, node: Node) -> ResultOrError:
        func = cast(FunctionEvaluation, node.value)
        
        f = None
        for i in range(len(builtin_functions)):
            name, _, _ =  builtin_functions[i]
            if name == func.name:
                f = builtin_functions[i]
                break
        
        if f == None:
            return None, EvaluatorException(EvaluatorExceptionOptions(node, f"Function {func.name} is not builtin"))
    
        xs = [] 
        for value in func.values:
            v, err = self.__evaluate_node_with_map(value)
            if err:
                return None, err
            
            xs.append(v)
        
        _, y, params_count = f

        try:   
            if params_count == 1:
                return y(xs[0]), None
        except Exception:
            return None, EvaluatorException(EvaluatorExceptionOptions(node, f"Failed to evaluate function {name} at {xs}"))

    def __evaluate_function_at(self, func: Function, values: list[Node]) -> ResultOrError:
        vs = dict()
        
        for index, param in enumerate(func.params):
            id = cast(str, param.value)

            res, err = self.__evaluate_node_with_map(values[index])
            if err:
                return None, err

            vs.setdefault(id, res)

        self.stack.push(func.name, vs)
        
        value, err = self.__evaluate_node_with_map(func.body)
        if err:
            return None, err

        self.stack.pop()
        return value, None


    def __evaluate_function_eval(self, node: Node) -> ResultOrError:
        func_eval = cast(FunctionEvaluation, node.value)

        if func_eval.isbuiltin:
            return self.__evaluate_builtin_function(node)

        func = self.context.findfunc(func_eval.name)
        if not func:    
            return None, EvaluatorException(EvaluatorExceptionOptions(node, f"function {func_eval.name} not defined"))

        if len(func.params) != len(func_eval.values):
            return None, EvaluatorException(EvaluatorExceptionOptions(node, f"function {func_eval.name} expects {len(func.params)} parameter{'s' if (len(func.params) != 1) else ''} but {len(func_eval.values)} {'were' if (len(func_eval.values) > 1) else 'was'} given"))

        return self.__evaluate_function_at(func, func_eval.values)

    def __evaluate_function_body_parts(self, params: list[str], v: Node) -> EvaluatorException | None:
        if v.kind == NodeKind.FLOAT:
            return None
        
        if v.kind == NodeKind.INTEGER:
            return None

        if v.kind == NodeKind.BINARY_OPERATION:
            err =  self.__evaluate_function_body_parts(params, cast(BinOperation, v.value).left)
            if err:
                return err
            
            err = self.__evaluate_function_body_parts(params, cast(BinOperation, v.value).right)
            if err:
                return err
            
            return None
    
        if v.kind == NodeKind.IDENTIFIER:
            if cast(str, v.value) in params:
                return None
            
            return EvaluatorException(EvaluatorExceptionOptions(v, f"Identifier {cast(str, v.value)} not found")) 

        if v.kind == NodeKind.FUNCTION_EVALUATION:
            func = cast(FunctionEvaluation, v.value)
            if func.isbuiltin:
                return None
            
            found = self.context.findfunc(func.name)
            
            if not found:
                return EvaluatorException(EvaluatorExceptionOptions(v, f"function `{func.name}` doesn't exist"))
            
            params_count = len(found.params)
            if params_count != len(func.values):
                return EvaluatorException(EvaluatorExceptionOptions(v, f"function `{func.name}` expects {params_count} args, but {len(func.values)} were given"))

            for param in found.params:
                err = self.__evaluate_function_body_parts(params, param)
                if err:
                    return err
                
            return None

        raise NotImplementedError()

    def __evaluate_function_declaration(self, node: Node) -> ResultOrError:
        func = cast(FunctionDeclaration, node.value)

        if self.context.funcexists(func.name):
            return None, EvaluatorException(EvaluatorExceptionOptions(node, f"function `{func.name}` already defined"))


        params = [cast(str, v.value) for v in func.variables]
        err = self.__evaluate_function_body_parts(params, func.body)
        if err:
            return None, err
        
        self.context.definefunc(Function(func.name, func.variables, func.body))
        
        vs = [v.value for v in func.variables]
        
        s = "["
        for i, v in enumerate(vs):
            s += f"{v}"
            if i != len(vs) - 1:
                s += ", "
        s += "]"

        return f"{func.name}({s})", None

    def __evaluate_draw_command(self, node: Node) -> ResultOrError:
        cmd = cast(DrawFunction, node.value)

        func = self.context.findfunc(cmd.func)
        if func == None:
            return None, EvaluatorException(EvaluatorExceptionOptions(node, f"Function {cmd.func} not defined"))
        
        if len(func.params) != 1:
            return None, EvaluatorException(EvaluatorExceptionOptions(node, f"Drawing multi-dimensional functions is not supported"))

        lower, err = self.__evaluate_node(cmd._from)
        if err:
            return None, err

        upper, err = self.__evaluate_node(cmd._to)
        if err:
            return None, err

        step, err = self.__evaluate_node(cmd.step)
        if err:
            return None, err
        
        lower = cast(float, lower)
        upper = cast(float, upper)
        step  = cast(float, step)

        if lower > upper:
            return None, EvaluatorException(EvaluatorExceptionOptions(node, f"the lower bound should be greater than the upper bound: {lower} > {upper}"))
        
        if step == 0:
            step = 0.1

        param = func.params[0]
        id = cast(str, param.value) 

        xs = []
        ys = []

        vs = dict()
        
        x = lower
        while x <= upper:
            xs.append(x)

            vs[id] = x
            self.stack.push(func.name, vs)
            
            value, err = self.__evaluate_node_with_map(func.body)
            ys.append(value if err == None else None)
            
            self.stack.pop()
            x += step

        try:
            Drawer.draw(DrawerInput(func.name, id, xs, ys))
        except Exception:
            pass

        return "done", None

    def __evaluate_node(self, node: Node):
        if node.kind == NodeKind.BINARY_OPERATION:
            return self.__evaluate_binop(node)
        
        if node.kind == NodeKind.FLOAT:
            return self.__evaluate_float(node)
    
        if node.kind == NodeKind.INTEGER:
            return self.__evaluate_int(node)

        if node.kind == NodeKind.FUNCTION_DECLARATION:
            return self.__evaluate_function_declaration(node)
    
        if node.kind == NodeKind.FUNCTION_EVALUATION:
            return self.__evaluate_function_eval(node)

        if node.kind == NodeKind.DRAW_FUNCTION:
            return self.__evaluate_draw_command(node)
        
        raise NotImplementedError()

    def __evaluate(self, tree: AST):
        root = tree.root
        return self.__evaluate_node(root)

    def __evaluate_local(self) -> ResultOrError:
        return self.__evaluate(self.tree)

    def eval(self) -> ResultOrError:
        result, err = self.__evaluate_local()
        
        if err:
            return None, err

        return result, None