%{
#include <stdio.h>
#include <stdlib.h>

void yyerror(const char *s);
int yylex(void);

extern FILE *yyin;
extern int yylineno;
%}

%token WHILE PRINT IDENTIFIER NUMBER
%token INC DEC LT GT LE GE EQ NE
%token LPAREN RPAREN SEMICOLON

%%

program:
    statement
    ;

statement:
      WHILE LPAREN condition RPAREN statement
    | PRINT LPAREN expression RPAREN SEMICOLON
    | expression SEMICOLON
    ;

condition:
    expression comparison_op expression
    ;

expression:
      primary
    | INC IDENTIFIER
    | DEC IDENTIFIER
    ;

primary:
      IDENTIFIER
    | NUMBER
    ;

comparison_op:
      LT
    | GT
    | LE
    | GE
    | EQ
    | NE
    ;

%%

void yyerror(const char *s)
{
    fprintf(stderr, "Синтаксическая ошибка (строка %d): %s\n", yylineno, s);
}
