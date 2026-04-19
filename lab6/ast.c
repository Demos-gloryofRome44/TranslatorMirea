#include <stdlib.h>
#include <string.h>
#include "ast.h"

static Node *alloc_node(NodeType t)
{
    Node *n = (Node *)calloc(1, sizeof(Node));
    n->type = t;
    return n;
}

Node *node_while(Node *cond, Node *body)
{
    Node *n = alloc_node(NODE_WHILE);
    n->u.while_stmt.cond = cond;
    n->u.while_stmt.body = body;
    return n;
}

Node *node_print(Node *expr)
{
    Node *n = alloc_node(NODE_PRINT);
    n->u.print_stmt.expr = expr;
    return n;
}

Node *node_expr_stmt(Node *expr)
{
    Node *n = alloc_node(NODE_EXPR_STMT);
    n->u.expr_stmt.expr = expr;
    return n;
}

Node *node_condition(Node *left, int op, Node *right)
{
    Node *n = alloc_node(NODE_CONDITION);
    n->u.condition.left = left;
    n->u.condition.right = right;
    n->u.condition.op = op;
    return n;
}

Node *node_increment(char *name, int delta)
{
    Node *n = alloc_node(NODE_INCREMENT);
    n->u.incr.name = name;
    n->u.incr.delta = delta;
    return n;
}

Node *node_identifier(char *name)
{
    Node *n = alloc_node(NODE_IDENTIFIER);
    n->u.ident.name = name;
    return n;
}

Node *node_number(double value)
{
    Node *n = alloc_node(NODE_NUMBER);
    n->u.number.value = value;
    return n;
}

void node_free(Node *n)
{
    if (!n) return;
    switch (n->type) {
        case NODE_WHILE:
            node_free(n->u.while_stmt.cond);
            node_free(n->u.while_stmt.body);
            break;
        case NODE_PRINT:
            node_free(n->u.print_stmt.expr);
            break;
        case NODE_EXPR_STMT:
            node_free(n->u.expr_stmt.expr);
            break;
        case NODE_CONDITION:
            node_free(n->u.condition.left);
            node_free(n->u.condition.right);
            break;
        case NODE_INCREMENT:
            free(n->u.incr.name);
            break;
        case NODE_IDENTIFIER:
            free(n->u.ident.name);
            break;
        case NODE_NUMBER:
            break;
    }
    free(n);
}
