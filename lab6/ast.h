#ifndef AST_H
#define AST_H

typedef enum {
    NODE_WHILE,
    NODE_PRINT,
    NODE_EXPR_STMT,
    NODE_CONDITION,
    NODE_INCREMENT,
    NODE_IDENTIFIER,
    NODE_NUMBER
} NodeType;

typedef enum {
    OP_LT, OP_GT, OP_LE, OP_GE, OP_EQ, OP_NE
} CompOp;

typedef struct Node {
    NodeType type;
    int line;
    union {
        struct { struct Node *cond; struct Node *body; } while_stmt;
        struct { struct Node *expr; } print_stmt;
        struct { struct Node *expr; } expr_stmt;
        struct { struct Node *left; struct Node *right; int op; } condition;
        struct { char *name; int delta; } incr;
        struct { char *name; } ident;
        struct { double value; } number;
    } u;
} Node;

Node *node_while(Node *cond, Node *body);
Node *node_print(Node *expr);
Node *node_expr_stmt(Node *expr);
Node *node_condition(Node *left, int op, Node *right);
Node *node_increment(char *name, int delta);
Node *node_identifier(char *name);
Node *node_number(double value);

void node_free(Node *n);

#endif
