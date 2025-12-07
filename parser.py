from scanner import Scanner, TokenType, Token

"""
Синтаксический анализатор (парсер)
Рекурсивный нисходящий предикативный распознаватель
"""

class ParseError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
    
    def parse(self):
        try:
            return self.program()
        except ParseError as e:
            print(f"Ошибка парсинга: {e}")
            return None
    
    def program(self):
        """<Program> ::= <Statement>"""
        result = self.statement()
        
        if not self.is_at_end():
            self.error("Ожидается конец программы")
        
        return result
    
    def statement(self):
        """<Statement> ::= <While> | <Print> | <Expression> ";" """
        if self.match(TokenType.WHILE):
            return self.while_statement()
        elif self.match(TokenType.PRINT):
            return self.print_statement()
        else:
            expr = self.expression()
            self.consume(TokenType.SEMICOLON, "Ожидается ';' после выражения")
            return ('expression_stmt', expr)
    
    def while_statement(self):
        """<While> ::= "while" "(" <Condition> ")" <Statement> """
        self.consume(TokenType.LPAREN, "Ожидается '(' после 'while'")
        condition = self.condition()
        self.consume(TokenType.RPAREN, "Ожидается ')' после условия")
        body = self.statement()
        return ('while', condition, body)
    
    def condition(self):
        """<Condition> ::= <Expression> <ComparisonOp> <Expression> """
        left = self.expression()
        op = self.comparison_op()
        right = self.expression()
        return ('condition', left, op, right)
    
    def comparison_op(self):
        """<ComparisonOp> ::= "<" | ">" | "<=" | ">=" | "==" | "!=" """
        if self.match(TokenType.LESS):
            return '<'
        elif self.match(TokenType.GREATER):
            return '>'
        elif self.match(TokenType.LESSEQ):
            return '<='
        elif self.match(TokenType.GREATEREQ):
            return '>='
        elif self.match(TokenType.EQUAL):
            return '=='
        elif self.match(TokenType.NOTEQUAL):
            return '!='
        else:
            self.error("Ожидается оператор сравнения")
    
    def expression(self):
        """<Expression> ::= <Primary> | "++" identifier | "--" identifier """
        if self.match(TokenType.PLUSPLUS):
            ident = self.consume(TokenType.IDENTIFIER, "Ожидается идентификатор после '++'")
            return ('increment', 'pre', ident.value, 1)
        elif self.match(TokenType.MINUSMINUS):
            ident = self.consume(TokenType.IDENTIFIER, "Ожидается идентификатор после '--'")
            return ('increment', 'pre', ident.value, -1)
        else:
            return self.primary()
    
    def primary(self):
        """<Primary> ::= identifier | number """
        if self.match(TokenType.IDENTIFIER):
            return ('identifier', self.previous().value)
        elif self.match(TokenType.NUMBER):
            return ('number', self.previous().value)
        else:
            self.error("Ожидается идентификатор или число")
    
    def print_statement(self):
        """<Print> ::= "print" "(" <Expression> ")" ";" """
        self.consume(TokenType.LPAREN, "Ожидается '(' после 'print'")
        expr = self.expression()
        self.consume(TokenType.RPAREN, "Ожидается ')' после выражения")
        self.consume(TokenType.SEMICOLON, "Ожидается ';' после print")
        return ('print', expr)
    
    # Вспомогательные методы парсера
    
    def match(self, *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False
    
    def consume(self, type, message):
        if self.check(type):
            return self.advance()
        self.error(message)
    
    def check(self, type):
        if self.is_at_end():
            return False
        return self.peek().type == type
    
    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()
    
    def previous(self):
        return self.tokens[self.current - 1]
    
    def peek(self):
        return self.tokens[self.current]
    
    def is_at_end(self):
        return self.peek().type == TokenType.EOF
    
    def error(self, message):
        token = self.peek()
        raise ParseError(f"[Строка {token.line}, Колонка {token.column}] {message}")