"""
Лексический анализатор (сканер)
Преобразует поток символов в токены
"""

class TokenType:
    WHILE = "WHILE"
    PRINT = "PRINT"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    PLUSPLUS = "PLUSPLUS"
    MINUSMINUS = "MINUSMINUS"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    SEMICOLON = "SEMICOLON"
    LESS = "LESS"
    GREATER = "GREATER"
    LESSEQ = "LESSEQ"
    GREATEREQ = "GREATEREQ"
    EQUAL = "EQUAL"
    NOTEQUAL = "NOTEQUAL"
    EOF = "EOF"

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type}, '{self.value}', {self.line}:{self.column})"


class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.keywords = {
            'while': TokenType.WHILE,
            'print': TokenType.PRINT
        }
        self.single_char_operators = {
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            ';': TokenType.SEMICOLON,
            '<': TokenType.LESS,
            '>': TokenType.GREATER
        }
        self.double_char_operators = {
            '++': TokenType.PLUSPLUS,
            '--': TokenType.MINUSMINUS,
            '<=': TokenType.LESSEQ,
            '>=': TokenType.GREATEREQ,
            '==': TokenType.EQUAL,
            '!=': TokenType.NOTEQUAL
        }
    
    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens
    
    def scan_token(self):
        c = self.advance()
        
        if c == ' ' or c == '\t' or c == '\r':
            return
        elif c == '\n':
            self.line += 1
            self.column = 1
        elif c.isalpha():
            self.identifier()
        elif c.isdigit():
            self.number()
        elif c in self.single_char_operators or c in ['+', '-', '=', '!']:
            self.operator(c)
        else:
            self.error(f"Неожиданный символ: '{c}'")
    
    def identifier(self):
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()
        
        text = self.source[self.start:self.current]
        token_type = self.keywords.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type, text)
    
    def number(self):
        while self.peek().isdigit():
            self.advance()
        
        value = self.source[self.start:self.current]
        self.add_token(TokenType.NUMBER, int(value))
    
    def operator(self, c):
        if not self.is_at_end():
            next_char = self.peek()
            two_char = c + next_char
            if two_char in self.double_char_operators:
                self.advance()
                self.add_token(self.double_char_operators[two_char], two_char)
                return
        
        if c in self.single_char_operators:
            self.add_token(self.single_char_operators[c], c)
        elif c == '+':
            self.error(f"Ожидается '++', получен '{c}'")
        elif c == '-':
            self.error(f"Ожидается '--', получен '{c}'")
        elif c == '=':
            self.error(f"Ожидается '==', получен '{c}'")
        elif c == '!':
            self.error(f"Ожидается '!=', получен '{c}'")
    
    def add_token(self, type, value):
        text = str(value)
        self.tokens.append(Token(type, value, self.line, self.column - len(text)))
    
    def advance(self):
        self.current += 1
        self.column += 1
        return self.source[self.current - 1]
    
    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]
    
    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]
    
    def is_at_end(self):
        return self.current >= len(self.source)
    
    def error(self, message):
        raise SyntaxError(f"[Строка {self.line}, Колонка {self.column}] {message}")