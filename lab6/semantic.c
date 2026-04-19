#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "semantic.h"

#define MAX_ITERS 10000

typedef struct Var {
    char *name;
    double value;
    struct Var *next;
} Var;

static Var *vars = NULL;
static int had_error = 0;

static Var *find_var(const char *name)
{
    for (Var *v = vars; v; v = v->next) {
        if (strcmp(v->name, name) == 0) return v;
    }
    return NULL;
}

static Var *get_or_create(const char *name)
{
    Var *v = find_var(name);
    if (v) return v;
    v = (Var *)malloc(sizeof(Var));
    v->name = strdup(name);
    v->value = 0.0;
    v->next = vars;
    vars = v;
    return v;
}

static void print_number(double v)
{
    if (v == (long long)v) {
        printf("%lld\n", (long long)v);
    } else {
        printf("%g\n", v);
    }
}

static double eval_expr(Node *n);
static int    eval_cond(Node *n);
static void   exec_stmt(Node *n);

static double eval_expr(Node *n)
{
    switch (n->type) {
        case NODE_NUMBER:
            return n->u.number.value;
        case NODE_IDENTIFIER: {
            Var *v = get_or_create(n->u.ident.name);
            return v->value;
        }
        case NODE_INCREMENT: {
            Var *v = get_or_create(n->u.incr.name);
            v->value += n->u.incr.delta;
            return v->value;
        }
        default:
            fprintf(stderr, "Семантическая ошибка: неизвестный тип выражения\n");
            had_error = 1;
            return 0.0;
    }
}

static int eval_cond(Node *n)
{
    double l = eval_expr(n->u.condition.left);
    double r = eval_expr(n->u.condition.right);
    switch (n->u.condition.op) {
        case OP_LT: return l <  r;
        case OP_GT: return l >  r;
        case OP_LE: return l <= r;
        case OP_GE: return l >= r;
        case OP_EQ: return l == r;
        case OP_NE: return l != r;
    }
    return 0;
}

static void exec_stmt(Node *n)
{
    if (had_error || !n) return;
    switch (n->type) {
        case NODE_WHILE: {
            long iters = 0;
            while (eval_cond(n->u.while_stmt.cond)) {
                if (++iters > MAX_ITERS) {
                    fprintf(stderr,
                        "Семантическая ошибка: превышен лимит итераций цикла (%d)\n",
                        MAX_ITERS);
                    had_error = 1;
                    return;
                }
                exec_stmt(n->u.while_stmt.body);
                if (had_error) return;
            }
            break;
        }
        case NODE_PRINT: {
            double v = eval_expr(n->u.print_stmt.expr);
            if (!had_error) print_number(v);
            break;
        }
        case NODE_EXPR_STMT:
            eval_expr(n->u.expr_stmt.expr);
            break;
        default:
            fprintf(stderr, "Семантическая ошибка: неизвестный оператор\n");
            had_error = 1;
    }
}

int semantic_run(Node *root)
{
    had_error = 0;
    if (!root) return 1;
    exec_stmt(root);
    return had_error ? 1 : 0;
}

void semantic_print_state(void)
{
    if (!vars) {
        printf("(нет переменных)\n");
        return;
    }
    for (Var *v = vars; v; v = v->next) {
        printf("%s = ", v->name);
        if (v->value == (long long)v->value)
            printf("%lld\n", (long long)v->value);
        else
            printf("%g\n", v->value);
    }
}

void semantic_reset(void)
{
    Var *v = vars;
    while (v) {
        Var *next = v->next;
        free(v->name);
        free(v);
        v = next;
    }
    vars = NULL;
    had_error = 0;
}
