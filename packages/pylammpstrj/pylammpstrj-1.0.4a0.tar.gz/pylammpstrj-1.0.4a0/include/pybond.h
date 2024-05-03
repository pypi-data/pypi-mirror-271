#ifndef _PY_BOND_H
#define _PY_BOND_H

#include "bond.h"

#include <Python.h>

#include <object.h>

enum BondMode parse_bond_mode(long input_bond_mode);

enum BondSelection parse_bond_selection(long input_selection);

union BondField parse_bond_field(PyObject *input_field, enum BondSelection selection);

struct BondTable parse_bond_table(PyObject *list, int by_type);

#endif
