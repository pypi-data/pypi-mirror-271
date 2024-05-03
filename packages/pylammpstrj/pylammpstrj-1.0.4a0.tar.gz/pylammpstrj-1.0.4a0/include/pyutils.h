#ifndef _PYUTILS_H
#define _PYUTILS_H

#include "atom.h"
#include "select.h"

#include <Python.h>

#include <object.h>

enum Operator parse_operator(const long input_op);

unsigned int parse_field_name(const struct AtomBuilder atom_builder, const char *field_name, enum SelectionType *type);

union SelectionValue parse_selection_value(const enum SelectionType type, const struct AtomBuilder builder, const unsigned int field, PyObject *input_value);

#endif
