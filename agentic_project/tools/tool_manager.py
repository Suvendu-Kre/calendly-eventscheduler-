from langchain_core.tools import tool
import ast
import math

@tool
def calculate(expression: str) -> str:
    """Evaluate a math expression safely."""
    try:
        node = ast.parse(expression, mode='eval')
        # Only allow safe operations
        safe_ops = {ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub}
        safe_funcs = {
            'sqrt': math.sqrt,
            'pow': math.pow,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'exp': math.exp,
            'log': math.log,
            'log10': math.log10
        }

        class SafeEvaluator(ast.NodeVisitor):
            def visit_Name(self, node):
                if node.id not in safe_funcs:
                    raise NameError(f"Use of unknown name {node.id}")
            def visit_Call(self, node):
                 if not isinstance(node.func, ast.Name) or node.func.id not in safe_funcs:
                    raise NameError(f"Use of unknown function {node.func.id}")
                 self.generic_visit(node)
            def visit_BinOp(self, node):
                if type(node.op) not in safe_ops:
                    raise TypeError(f"Unsafe operator {node.op}")
                self.generic_visit(node)

        SafeEvaluator().visit(node)
        code = compile(node, '<string>', 'eval')
        result = eval(code, {'__builtins__': None}, safe_funcs)
        return str(result)
    except Exception as e:
        return f"Error: {e}"

def get_tools():
    return [calculate]