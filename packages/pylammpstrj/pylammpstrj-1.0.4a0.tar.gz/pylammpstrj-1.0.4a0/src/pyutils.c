#define PY_SSIZE_T_CLEAN

#include "atom.h"
#include "bond.h"
#include "select.h"

#include <errno.h>
#include <Python.h>
#include <stdio.h>
#include <string.h>

#include <floatobject.h>
#include <longobject.h>
#include <object.h>
#include <pyerrors.h>
#include <unicodeobject.h>
#include <warnings.h>
#include <abstract.h>

enum Operator parse_operator(const long input_op)
{
    enum Operator op = (enum Operator) input_op;
    if (op < 1 || 5 < op)  // Assuming there are only 4 comparison operators
        PyErr_SetString(PyExc_RuntimeError, "Invalid operator: pylammpstrj operators should be used.");
    return op;
}

unsigned int parse_field_name(const struct AtomBuilder atom_builder, const char *field_name, enum SelectionType *type)
{
    // Atom fields
    *type = SELECTION_FIELDS;
    for (unsigned int f = 0; f < atom_builder.N_fields; f++)
        if (strcmp(field_name, atom_builder.field_names[f]) == 0) return f;

    // Atom bonds
    *type = SELECTION_BONDS;
    if (strcmp(field_name, "N_bonds") == 0) return BS_N_BONDS;
    if (strcmp(field_name, "bond_order") == 0) return BS_TOTAL_BO;

    *type = SELECTION_NULL;
    PyErr_SetString(PyExc_RuntimeError, "Attribute does not match any attribute.");
    return 0;
}

union SelectionValue parse_selection_value(const enum SelectionType type, const struct AtomBuilder builder, const unsigned int field,
                                           PyObject *input_value)
{
    union SelectionValue value = {0};

    switch (type)
    {
        case SELECTION_FIELDS:
            switch (builder.fields_types[field])
            {
                case AFT_INT:
                    if (PyObject_TypeCheck(input_value, &PyLong_Type))
                        value.i = PyLong_AsLong(input_value);
                    else
                        PyErr_SetString(PyExc_RuntimeError, "Wrong attribute type for selection");
                    break;
                case AFT_DOUBLE:
                    if (PyObject_TypeCheck(input_value, &PyFloat_Type))
                        value.d = PyFloat_AsDouble(input_value);
                    else if (PyObject_TypeCheck(input_value, &PyLong_Type))
                        value.d = PyLong_AsDouble(input_value);
                    else
                        PyErr_SetString(PyExc_RuntimeError, "Wrong attribute type for selection");
                    break;
                case AFT_STRING:
                    if (PyObject_TypeCheck(input_value, &PyUnicode_Type))
                        strncpy(value.s, PyUnicode_AsUTF8(input_value), VALUE_STR_LIMIT);
                    else
                        PyErr_SetString(PyExc_RuntimeError, "Wrong attribute type for selection");
                    break;
                default:
                    errno = EINVAL;
                    perror("Error while checking the field selection type (parse_selection_value.field)");
                    break;
            }
            break;
        case SELECTION_BONDS:
            switch (field)
            {
                case BS_N_BONDS:
                    if (PyObject_TypeCheck(input_value, &PyLong_Type))
                        value.i = PyLong_AsLong(input_value);
                    else
                        PyErr_SetString(PyExc_RuntimeError, "Wrong attribute type for selection");
                    break;
                case BS_TOTAL_BO:
                    if (PyObject_TypeCheck(input_value, &PyFloat_Type))
                        value.d = PyFloat_AsDouble(input_value);
                    else if (PyObject_TypeCheck(input_value, &PyLong_Type))
                        value.d = PyLong_AsDouble(input_value);
                    else
                        PyErr_SetString(PyExc_RuntimeError, "Wrong attribute type for selection");
                    break;
                default:
                    errno = EINVAL;
                    perror("Error while checking bond selection attribute (parse_selection_value.field)");
                    break;
            }
            break;
        default:
            errno = EINVAL;
            perror("Error while checking the selection type (parse_selection_value.type)");
            break;
    }

    return value;
}
