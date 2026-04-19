%{
#include <stdio.h>
#include <stdlib.h>
#include "ast.h"

void yyerror(const char *s);
int  yylex(void);

extern FILE *yyin;
extern int   yylineno;

Node *ast_root = NULL;
%}

%union {
    double  dval;
    char   *sval;
    int     op;
    struct Node *node;
}

%token WHILE PRINT
%token <sval> IDENTIFIER
%token <dval> NUMBER
%token INC DEC
%token LT GT LE GE EQ NE
%token LPAREN RPAREN SEMICOLON

%type <node> program statement condition expression primary
%type <op>   comparison_op

%%

program:
    statement                                   { ast_root = $1; }
    ;

statement:
      WHILE LPAREN condition RPAREN statement   { $$ = node_while($3, $5); }
    | PRINT LPAREN expression RPAREN SEMICOLON  { $$ = node_print($3); }
    | expression SEMICOLON                      { $$ = node_expr_stmt($1); }
    ;

condition:
    expression comparison_op expression         { $$ = node_condition($1, $2, $3); }
    ;

expression:
      primary                                   { $$ = $1; }
    | INC IDENTIFIER                            { $$ = node_increment($2, +1); }
    | DEC IDENTIFIER                            { $$ = node_increment($2, -1); }
    ;

primary:
      IDENTIFIER                                { $$ = node_identifier($1); }
    | NUMBER                                    { $$ = node_number($1); }
    ;

comparison_op:
      LT { $$ = OP_LT; }
    | GT { $$ = OP_GT; }
    | LE { $$ = OP_LE; }
    | GE { $$ = OP_GE; }
    | EQ { $$ = OP_EQ; }
    | NE { $$ = OP_NE; }
    ;

%%

void yyerror(const char *s)
{
    fprintf(stderr, "Синтаксическая ошибка (строка %d): %s\n", yylineno, s);
}
