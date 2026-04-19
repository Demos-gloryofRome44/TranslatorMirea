#include <stdio.h>
#include <stdlib.h>
#include "ast.h"
#include "semantic.h"

extern FILE *yyin;
extern int   yyparse(void);
extern Node *ast_root;

int main(int argc, char *argv[])
{
    if (argc < 2) {
        fprintf(stderr, "Использование: %s <файл с исходным текстом>\n", argv[0]);
        return 1;
    }

    FILE *f = fopen(argv[1], "r");
    if (!f) {
        perror(argv[1]);
        return 1;
    }

    yyin = f;
    int rc = yyparse();
    fclose(f);

    if (rc != 0) {
        return rc;
    }

    printf("Синтаксический разбор завершён успешно: файл \"%s\" соответствует грамматике.\n",
           argv[1]);

    printf("\n=== Выполнение ===\n");
    int serr = semantic_run(ast_root);

    printf("\n=== Состояние переменных ===\n");
    semantic_print_state();

    node_free(ast_root);
    ast_root = NULL;
    semantic_reset();
    return serr;
}
