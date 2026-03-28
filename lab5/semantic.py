"""
Семантический анализатор
Выполнение программы с состоянием переменных
"""

class SemanticError(Exception):
    pass

class SemanticAnalyzer:
    def __init__(self):
        self.variables = {}
    
    def execute(self, ast):
        if ast is None:
            return
        
        node_type = ast[0]
        
        if node_type == 'while':
            self.execute_while(ast)
        elif node_type == 'print':
            self.execute_print(ast)
        elif node_type == 'expression_stmt':
            self.evaluate(ast[1])
        else:
            raise SemanticError(f"Неизвестный тип узла: {node_type}")
    
    def execute_while(self, node):
        _, condition, body = node
        
        while self.evaluate_condition(condition):
            self.execute(body)
    
    def execute_print(self, node):
        _, expr = node
        value = self.evaluate(expr)
        print(value)
    
    def evaluate_condition(self, node):
        _, left_expr, op, right_expr = node
        left = self.evaluate(left_expr)
        right = self.evaluate(right_expr)
        
        if op == '<':
            return left < right
        elif op == '>':
            return left > right
        elif op == '<=':
            return left <= right
        elif op == '>=':
            return left >= right
        elif op == '==':
            return left == right
        elif op == '!=':
            return left != right
        else:
            raise SemanticError(f"Неизвестный оператор сравнения: {op}")
    
    def evaluate(self, expr):
        expr_type = expr[0]
        
        if expr_type == 'number':
            return expr[1]
        elif expr_type == 'identifier':
            var_name = expr[1]
            if var_name in self.variables:
                return self.variables[var_name]
            else:
                self.variables[var_name] = 0
                return 0
        elif expr_type == 'increment':
            _, timing, var_name, delta = expr
            current = self.variables.get(var_name, 0)
            
            if timing == 'pre':
                new_value = current + delta
                self.variables[var_name] = new_value
                return new_value
            else:
                self.variables[var_name] = current + delta
                return current
        else:
            raise SemanticError(f"Неизвестный тип выражения: {expr_type}")