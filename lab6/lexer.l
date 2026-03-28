%{
#include <stdio.h>
#include <stdlib.h>
#include "y.tab.h"
%}

%option yylineno noyywrap

%%

[ \t\r\n]+    ;

"while"       { return WHILE; }
"print"       { return PRINT; }

"<="          { return LE; }
">="          { return GE; }
"=="          { return EQ; }
"!="          { return NE; }
"++"          { return INC; }
"--"          { return DEC; }

"<"           { return LT; }
">"           { return GT; }

"("           { return LPAREN; }
")"           { return RPAREN; }
";"           { return SEMICOLON; }

[0-9]+"."[0-9]* |
[0-9]*"."[0-9]+ |
[0-9]+[eE][+-]?[0-9]+ |
[0-9]+"."[0-9]*[eE][+-]?[0-9]+ {
    return NUMBER;
}

[0-9]+        { return NUMBER; }

[a-zA-Z_][a-zA-Z0-9_]* {
    return IDENTIFIER;
}

. {
    fprintf(stderr,
            "Лексическая ошибка (строка %d): недопустимый символ '%s'\n",
            yylineno, yytext);
    exit(1);
}

%%
