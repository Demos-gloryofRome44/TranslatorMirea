#ifndef SEMANTIC_H
#define SEMANTIC_H

#include "ast.h"

int  semantic_run(Node *root);
void semantic_print_state(void);
void semantic_reset(void);

#endif
