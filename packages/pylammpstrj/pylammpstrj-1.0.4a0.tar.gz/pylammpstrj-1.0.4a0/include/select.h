#ifndef _SELECT_H
#define _SELECT_H

#include "atom.h"

#include <stdio.h>

enum SelectionType
{
    SELECTION_NULL,
    SELECTION_FIELDS,
    SELECTION_BONDS
};

enum Operator
{
    OPERATOR_NULL,
    OPERATOR_LT,
    OPERATOR_LEQ,
    OPERATOR_EQ,
    OPERATOR_GEQ,
    OPERATOR_GT
};

#define VALUE_STR_LIMIT 10

union SelectionValue
{
    int i;
    double d;
    char s[VALUE_STR_LIMIT];
};

struct Selection
{
    enum SelectionType type;
    unsigned int field;
    enum Operator op;
    union SelectionValue value;
};

void selection_parse_atom_selection(const struct Selection *selection, const struct AtomBuilder builder, size_t *offset, int (**to_select)(const void *, const void *), void **value_ptr);

void selection_parse_bond_selection(const struct Selection *selection, size_t *offset, int (**to_select)(const void *, const void *), void **value_ptr);

#endif
