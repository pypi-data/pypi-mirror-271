#define PY_SSIZE_T_CLEAN
#include "pybond.h"
#include "atom.h"
#include "bond.h"

#include <errno.h>
#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <floatobject.h>
#include <longobject.h>
#include <object.h>
#include <pyerrors.h>
#include "listobject.h"
#include "modsupport.h"

enum BondMode parse_bond_mode(long input_bond_mode)
{
    enum BondMode bond_mode = (enum BondMode) input_bond_mode;
    switch (bond_mode)
    {
        case BM_ID:
            break;
        case BM_BOND_ORDER:
            break;
        case BM_FULL:
            break;
        // case BM_NULL:
        default:
            PyErr_SetString(PyExc_RuntimeError, "Bond mode not handled (parse_bond_mode)");
            return 0;
    }

    return bond_mode;
}

enum BondSelection parse_bond_selection(long input_selection)
{
    enum BondSelection selection = (enum BondSelection) input_selection;
    switch (selection)
    {
        case BS_N_BONDS:
            break;
        case BS_TOTAL_BO:
            break;
        // case BS_TYPES_ALL:
        // case BS_TYPES_ANY:
        default:
            PyErr_SetString(PyExc_RuntimeError, "Bond selection not handled (parse_bond_selection)");
            return 0;
    }

    return selection;
}

union BondField parse_bond_field(PyObject *input_field, enum BondSelection selection)
{
    union BondField value = {0};

    switch (selection)
    {
        case BS_N_BONDS:
            if (!PyObject_TypeCheck(input_field, &PyLong_Type))
            {
                PyErr_SetString(PyExc_RuntimeError, "Argument value does not match selection type.");
                return (union BondField){0};
            }
            value.i = (unsigned int) PyLong_AsLong(input_field);
            break;
        case BS_TOTAL_BO:
            if (PyObject_TypeCheck(input_field, &PyFloat_Type))
                value.d = PyFloat_AsDouble(input_field);
            else if (PyObject_TypeCheck(input_field, &PyLong_Type))
                value.d = PyLong_AsDouble(input_field);
            else
            {
                PyErr_SetString(PyExc_RuntimeError, "Argument value does not match selection type.");
                return (union BondField){0};
            }
            break;
        // case BS_TYPES_ALL:
        // case BS_TYPES_ANY:
        default:
            PyErr_SetString(PyExc_RuntimeError, "Bond selection not handled (parse_bond_selection)");
            break;
    }
    return value;
}

struct BondTable parse_bond_table(PyObject *list, int by_type)
{
    // Preparing to parse the bond table
    struct BondTable table = {0};
    unsigned int N_entries = (unsigned int) PyList_Size(list);

    struct BondTableEntry *entries = calloc(N_entries, sizeof(struct BondTableEntry));
    if (entries == NULL)  // Could not allocate memory
    {
        errno = ENOMEM;
        perror("Error while allocating memory (parse_bond_table)");
        PyErr_SetFromErrno(PyExc_RuntimeError);
        return table;
    }

    // Parsing the bond table entries
    if (by_type)
        for (unsigned int e = 0; e < N_entries; e++)
        {
            unsigned int t1 = 0, t2 = 0;
            double length = 0.;

            if (!PyArg_ParseTuple(PyList_GetItem(list, e), "IId", &t1, &t2, &length))
            {
                free(entries);
                PyErr_SetString(PyExc_RuntimeError, "Error while parsing the arguments (parse_bond_table)");
                return table;
            }

            entries[e] = (struct BondTableEntry){.atoms = {{.type = t1}, {.type = t2}}, .length = length};
        }
    else
        for (unsigned int e = 0; e < N_entries; e++)
        {
            char *e1, *e2;
            struct BondTableEntry *entry = entries + e;
            double length = 0.;

            if (!PyArg_ParseTuple(PyList_GetItem(list, e), "ssd", &e1, &e2, &length) || strlen(e1) >= LABEL_LIMIT ||
                strlen(e2) >= LABEL_LIMIT)
            {
                free(entries);
                PyErr_SetString(PyExc_RuntimeError, "Error while parsing the arguments (parse_bond_table)");
                return table;
            }

            strncpy(entry->atoms[0].element, e1, LABEL_LIMIT);
            strncpy(entry->atoms[1].element, e2, LABEL_LIMIT);
            entry->length = length;
        }

    // Transfering the data
    table.N_entries = N_entries;
    table.entries = entries;

    return table;
}
