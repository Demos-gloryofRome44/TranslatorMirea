#include <stdio.h>
#include <stdlib.h>

extern FILE *yyin;
extern int yyparse(void);

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

    if (rc == 0) {
        printf("Разбор завершён успешно: файл \"%s\" соответствует грамматике.\n",
               argv[1]);
    }

    return rc;
}
