#define PY_SSIZE_T_CLEAN

#include "pytrajectory.h"
#include "atom.h"
#include "bond.h"
#include "pyatom.h"
#include "pybond.h"
#include "pybox.h"
#include "pyutils.h"
#include "select.h"
#include "trajectory.h"
#include "utils.h"

#include <errno.h>
#include <Python.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include <bytesobject.h>
#include <descrobject.h>
#include <floatobject.h>
#include <listobject.h>
#include <longobject.h>
#include <methodobject.h>
#include <modsupport.h>
#include <object.h>
#include <pyerrors.h>
#include <pymacro.h>
#include <pyport.h>
#include <unicodeobject.h>

void PyTrajectory_dealloc(PyTrajectoryObject *self)
{
    trajectory_delete(&(self->trajectory));
    Py_TYPE(self)->tp_free((PyObject *) self);
}

PyObject *PyTrajectory_new(PyTypeObject *type, PyObject *Py_UNUSED(args), PyObject *Py_UNUSED(kwargs))
{
    PyTrajectoryObject *self;
    self = (PyTrajectoryObject *) type->tp_alloc(type, 0);
    return (PyObject *) self;
}

PyObject *PyTrajectory_get_N_configurations(PyTrajectoryObject *self, void *Py_UNUSED(closure))
{
    return (PyObject *) PyLong_FromLong(self->trajectory.N_configurations);
}

PyObject *PyTrajectory_get_steps(PyTrajectoryObject *self, void *Py_UNUSED(closure))
{
    unsigned long N_configurations = self->trajectory.N_configurations;
    unsigned int *steps = self->trajectory.steps;

    PyObject *list = PyList_New(N_configurations);
    for (unsigned int c = 0; c < N_configurations; c++) PyList_SetItem(list, c, PyLong_FromUnsignedLong((unsigned long) steps[c]));
    return list;
}

PyObject *PyTrajectory_get_N_atoms(PyTrajectoryObject *self, void *Py_UNUSED(closure))
{
    PyObject *list = PyList_New(self->trajectory.N_configurations);
    for (unsigned int c = 0; c < self->trajectory.N_configurations; c++)
        PyList_SetItem(list, c, PyLong_FromLong(self->trajectory.N_atoms[c]));
    return list;
}

PyObject *PyTrajectory_get_dump_format(PyTrajectoryObject *self, void *Py_UNUSED(closure))
{
    struct AtomBuilder atom_builder = self->trajectory.atom_builder;
    if (PyErr_Occurred()) return NULL;
    return PyUnicode_FromString(atom_builder.dump_format);
}

PyObject *PyTrajectory_get_field_names(PyTrajectoryObject *self, void *Py_UNUSED(closure))
{
    struct AtomBuilder atom_builder = self->trajectory.atom_builder;
    if (PyErr_Occurred()) return NULL;
    PyObject *list = PyList_New(atom_builder.N_fields);
    for (unsigned int f = 0; f < atom_builder.N_fields; f++) PyList_SetItem(list, f, PyUnicode_FromString(atom_builder.field_names[f]));
    return list;
}

PyObject *PyTrajectory_get_additional_fields(PyTrajectoryObject *self, void *Py_UNUSED(closure))
{
    struct AtomBuilder atom_builder = self->trajectory.atom_builder;
    if (PyErr_Occurred()) return NULL;

    PyObject *list = PyList_New(atom_builder.N_additional);
    for (unsigned int f = 0, fa = 0; f < atom_builder.N_fields; f++)
    {
        if (!atom_builder.is_additional[f]) continue;
        PyList_SetItem(list, fa, PyUnicode_FromString(atom_builder.field_names[f]));
        fa++;
    }
    return list;
}

PyObject *PyTrajectory_get_atoms(PyTrajectoryObject *self, void *Py_UNUSED(closure))
{
    PyObject *list = PyList_New(self->trajectory.N_configurations);
    if (list == NULL) return NULL;

    for (unsigned int c = 0, at = 0; c < self->trajectory.N_configurations; c++)
    {
        PyObject *inner_list = PyList_New(self->trajectory.N_atoms[c]);
        if (inner_list == NULL)
        {
            PyList_Type.tp_del(list);
            return NULL;
        }

        for (unsigned int a = 0; a < self->trajectory.N_atoms[c]; a++, at++)
        {
            PyAtomObject *atom = (PyAtomObject *) PyAtom_new(&PyAtomType, NULL, NULL);
            if (atom == NULL)
            {
                PyList_Type.tp_del(inner_list);
                PyList_Type.tp_del(list);
                return NULL;
            }

            PyAtom_initialize(atom, self, self->trajectory.atoms[at]);
            PyList_SetItem(inner_list, a, (PyObject *) atom);
        }
        PyList_SetItem(list, c, inner_list);
    }

    return list;
}

PyObject *PyTrajectory_get_boxes(PyTrajectoryObject *self, void *Py_UNUSED(closure))
{
    PyObject *list = PyList_New(self->trajectory.N_configurations);
    if (list == NULL) return NULL;

    for (unsigned int c = 0; c < self->trajectory.N_configurations; c++)
    {
        PyBoxObject *box = (PyBoxObject *) PyBox_new(&PyBoxType, NULL, NULL);
        if (box == NULL)
        {
            PyList_Type.tp_del(list);
            return NULL;
        }

        PyBox_initialize(box, self->trajectory.box[c]);
        PyList_SetItem(list, c, (PyObject *) box);
    }

    return list;
}

PyObject *PyTrajectory_get_bond_mode(PyTrajectoryObject *self, void *Py_UNUSED(closure))
{
    switch (self->trajectory.bond_builder.mode)
    {
        case BM_NULL:
            return PyUnicode_FromString("BM_NULL");
        case BM_ID:
            return PyUnicode_FromString("BM_ID");
        case BM_BOND_ORDER:
            return PyUnicode_FromString("BM_BOND_ORDER");
        case BM_FULL:
            return PyUnicode_FromString("BM_FULL");
        default:
            return NULL;
    }
}

PyGetSetDef PyTrajectory_getset[] = {
    {.name = "N_configurations", .get = (getter) PyTrajectory_get_N_configurations, .doc = "The number of configurations"},
    {.name = "steps", .get = (getter) PyTrajectory_get_steps, .doc = "The timesteps."},
    {.name = "N_atoms", .get = (getter) PyTrajectory_get_N_atoms, .doc = "The number of configurations"},
    {.name = "dump_format", .get = (getter) PyTrajectory_get_dump_format, .doc = "The dump format."},
    {.name = "field_names", .get = (getter) PyTrajectory_get_field_names, .doc = "The names of the fields."},
    {.name = "additional_fields", .get = (getter) PyTrajectory_get_additional_fields, .doc = "The additionnal fields."},
    {.name = "atoms", .get = (getter) PyTrajectory_get_atoms, .doc = "The atoms."},
    {.name = "boxes", .get = (getter) PyTrajectory_get_boxes, .doc = "The boxes."},
    {.name = "bond_mode", .get = (getter) PyTrajectory_get_bond_mode, .doc = "The bond reading mode."},
    {0}};

PyObject *PyTrajectory_str(PyTrajectoryObject *self)
{
    return PyUnicode_FromFormat("[%lu, %S, %s, %S, %S, %U, %R]", self->trajectory.N_configurations,
                                PyObject_Str(PyTrajectory_get_N_atoms(self, NULL)), PyObject_Str(PyTrajectory_get_dump_format(self, NULL)),
                                PyObject_Str(PyTrajectory_get_field_names(self, NULL)),
                                PyObject_Str(PyTrajectory_get_additional_fields(self, NULL)), PyTrajectory_get_bond_mode(self, NULL),
                                PyObject_Repr(PyTrajectory_get_atoms(self, NULL)));
}

PyObject *PyTrajectory_repr(PyTrajectoryObject *self)
{
    return PyUnicode_FromFormat(
        "trajectory(N_configurations=%lu N_atoms=%S dump_format='%s' "
        "field_names=%S is_additional=%S bond_mode=%U atoms=%R)",
        self->trajectory.N_configurations, PyObject_Str(PyTrajectory_get_N_atoms(self, NULL)),
        PyObject_Str(PyTrajectory_get_field_names(self, NULL)), PyObject_Str(PyTrajectory_get_dump_format(self, NULL)),
        PyObject_Str(PyTrajectory_get_additional_fields(self, NULL)), PyTrajectory_get_bond_mode(self, NULL),
        PyObject_Repr(PyTrajectory_get_atoms(self, NULL)));
}

void PyTrajectory_initialize(PyTrajectoryObject *self, struct Trajectory trajectory) { self->trajectory = trajectory; }

PyObject *PyTrajectory_select(PyTrajectoryObject *self, PyObject *args, PyObject *kwargs)
{
    // Preparing the variables
    char *kwlist[] = {"", "", "", "inplace", NULL};
    unsigned int field = 0;
    enum Operator op = 0;
    union SelectionValue value = {0};
    char *field_name = NULL;
    long input_op = 0;
    PyObject *input_value;  // Needs to be freed? NO
    int inplace = false;
    enum SelectionType type = 0;

    // Parsing the arguments
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "siO|$p", kwlist, &field_name, &input_op, &input_value, &inplace)) return NULL;

    field = parse_field_name(self->trajectory.atom_builder, field_name, &type);
    if (PyErr_Occurred()) return NULL;

    op = parse_operator(input_op);
    if (PyErr_Occurred()) return NULL;

    // value = parse_atom_field(self->trajectory.atom_builder, field, input_value);
    value = parse_selection_value(type, self->trajectory.atom_builder, field, input_value);
    if (PyErr_Occurred()) return NULL;

    if (!inplace)  // If the selection is not in place
    {
        // Preparing some more variables
        PyTrajectoryObject *new = (PyTrajectoryObject *) PyTrajectory_new(Py_TYPE(self), NULL, NULL);
        if (new == NULL) return NULL;
        struct Trajectory trajectory;

        // Actually selecting the atoms
        trajectory_select(&(self->trajectory), (struct Selection){.type = type, .field = field, .op = op, .value = value}, false,
                          &trajectory);
        if (errno != 0) return PyErr_SetFromErrno(PyExc_RuntimeError);

        PyTrajectory_initialize(new, trajectory);
        return (PyObject *) new;
    }

    // Actually selecting the atoms
    trajectory_select(&(self->trajectory), (struct Selection){.type = type, .field = field, .op = op, .value = value}, true, NULL);
    if (errno != 0) return PyErr_SetFromErrno(PyExc_RuntimeError);

    Py_RETURN_NONE;  // Need to return None otherwise it segfaults if the result is not assigned
}

PyObject *PyTrajectory_moving_select(PyTrajectoryObject *self, PyObject *args, PyObject *kwargs)
{
    // Preparing the variables
    char *kwlist[] = {"", "", "", "inplace", NULL};
    PyObject *names, *operators, *values;  // Needs to be freed? NO
    int inplace = false;

    // Parsing the arguments
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OOO|$p", kwlist, &names, &operators, &values, &inplace)) return NULL;

    struct Selection *selections = calloc(self->trajectory.N_configurations, sizeof(struct Selection));
    if (selections == NULL)
    {
        errno = ENOMEM;
        perror("Error while allocating memory (moving_select.selections)");
        PyErr_SetFromErrno(PyExc_RuntimeError);
        return NULL;
    }

    for (unsigned int c = 0; c < self->trajectory.N_configurations; c++)
    {
        selections[c].field = parse_field_name(self->trajectory.atom_builder, PyUnicode_AsUTF8(PyList_GetItem(names, c)), &(selections[c].type));
        if (PyErr_Occurred()) return NULL;

        selections[c].op = parse_operator(PyLong_AsLong(PyList_GetItem(operators, c)));
        if (PyErr_Occurred()) return NULL;

        selections[c].value = parse_selection_value(selections[c].type, self->trajectory.atom_builder, selections[c].field, PyList_GetItem(values, c));
        if (PyErr_Occurred()) return NULL;
    }

    // field = parse_field_name(self->trajectory.atom_builder, field_name, &type);
    // if (PyErr_Occurred()) return NULL;
    //
    // op = parse_operator(input_op);
    // if (PyErr_Occurred()) return NULL;
    //
    // // value = parse_atom_field(self->trajectory.atom_builder, field, input_value);
    // value = parse_selection_value(type, self->trajectory.atom_builder, field, input_value);
    // if (PyErr_Occurred()) return NULL;

    if (!inplace)  // If the selection is not in place
    {
        // Preparing some more variables
        PyTrajectoryObject *new = (PyTrajectoryObject *) PyTrajectory_new(Py_TYPE(self), NULL, NULL);
        if (new == NULL) return NULL;
        struct Trajectory trajectory;

        // Actually selecting the atoms
        trajectory_moving_select(&(self->trajectory), selections, false, &trajectory);
        if (errno != 0) return PyErr_SetFromErrno(PyExc_RuntimeError);

        PyTrajectory_initialize(new, trajectory);
        return (PyObject *) new;
    }

    // Actually selecting the atoms
    trajectory_moving_select(&(self->trajectory), selections, true, NULL);
    if (errno != 0) return PyErr_SetFromErrno(PyExc_RuntimeError);

    Py_RETURN_NONE;  // Need to return None otherwise it segfaults if the result is not assigned
}

PyObject *PyTrajectory_compute_average(PyTrajectoryObject *self, PyObject *args)
{
    char *field_name;
    if (!PyArg_ParseTuple(args, "s", &field_name)) return NULL;

    // Converting the field name
    enum SelectionType type = 0;
    unsigned int field = parse_field_name(self->trajectory.atom_builder, field_name, &type);
    if (PyErr_Occurred()) return NULL;

    // Computing the averages
    double *averages = trajectory_average_property(self->trajectory, field);
    if (errno != 0)  // Something went wrong
    {
        perror("Error while computing the average (PyTrajectory_compute_average)");
        return PyErr_SetFromErrno(PyExc_RuntimeError);
    }

    // Converting the array
    unsigned int N_configurations = self->trajectory.N_configurations;
    PyObject *list = PyList_New(N_configurations);
    if (PyErr_Occurred())
    {
        free(averages);
        return NULL;
    }

    for (unsigned int c = 0; c < N_configurations; c++) PyList_SetItem(list, c, PyFloat_FromDouble(averages[c]));

    // Finishing
    free(averages);
    return list;
}

PyObject *PyTrajectory_read_bonds(PyTrajectoryObject *self, PyObject *args)
{
    PyObject *bytes;
    char *file_name;
    Py_ssize_t length;
    long input_bond_mode;

    // Parsing the arguments
    if (!PyArg_ParseTuple(args, "O&i", PyUnicode_FSConverter, &bytes, &input_bond_mode)) return NULL;

    PyBytes_AsStringAndSize(bytes, &file_name, &length);
    if (length > FILE_NAME_LIMIT)
    {
        PyErr_SetString(PyExc_RuntimeError, "File name too long (PyTrajectory.read_bonds)");
        Py_DECREF(bytes);
        return NULL;
    }

    enum BondMode bond_mode = parse_bond_mode(input_bond_mode);
    if (PyErr_Occurred())
    {
        Py_DECREF(bytes);
        return NULL;
    }

    // Actually reading the bonds
    trajectory_read_bonds(file_name, bond_mode, &(self->trajectory));
    if (errno != 0)
    {
        PyErr_SetFromErrno(PyExc_RuntimeError);
        Py_DECREF(bytes);
        return NULL;
    }

    Py_DECREF(bytes);
    Py_RETURN_NONE;
}

PyObject *PyTrajectory_compute_bonds(PyTrajectoryObject *self, PyObject *args)
{
    // Preparing the parse the arguments
    PyObject *list;

    // Parsing the arguments
    if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &list)) return NULL;

    struct BondTable table = parse_bond_table(list, self->trajectory.atoms[0].type);
    if (PyErr_Occurred()) return NULL;

    trajectory_compute_bonds(&(self->trajectory), table);
    if (errno != 0)
    {
        bondtable_delete(&table);
        perror("Error while computing the bonds (PyTrajectory.compute_bonds)");
        PyErr_SetFromErrno(PyExc_RuntimeError);
        return NULL;
    }

    Py_RETURN_NONE;
}

PyMethodDef PyTrajectory_methods[] = {
    {"select", (PyCFunction) (void (*)(void)) PyTrajectory_select, METH_VARARGS | METH_KEYWORDS, "Select atoms."},
    {"moving_select", (PyCFunction) (void (*)(void)) PyTrajectory_moving_select, METH_VARARGS | METH_KEYWORDS, "Select atoms with moving selection."},
    {"average_property", (PyCFunction) PyTrajectory_compute_average, METH_VARARGS,
     "Computes the average of an atomic property throughout the simulation."},
    {"read_bonds", (PyCFunction) PyTrajectory_read_bonds, METH_VARARGS, "Read the bonds."},
    {"compute_bonds", (PyCFunction) PyTrajectory_compute_bonds, METH_VARARGS, "Compute the bonds from a bond table."},
    {0}};

PyTypeObject PyTrajectoryType = {.ob_base = PyVarObject_HEAD_INIT(NULL, 0)  // blabla
                                                .tp_name = "pylammpstrj.PyTrajectory",
                                 .tp_doc = "Trajectory objects",
                                 .tp_basicsize = sizeof(PyTrajectoryObject),
                                 .tp_itemsize = 0,
                                 .tp_flags = Py_TPFLAGS_DEFAULT,
                                 .tp_dealloc = (destructor) PyTrajectory_dealloc,
                                 .tp_new = PyTrajectory_new,
                                 .tp_getset = PyTrajectory_getset,
                                 .tp_methods = PyTrajectory_methods,
                                 .tp_str = (reprfunc) PyTrajectory_str,
                                 .tp_repr = (reprfunc) PyTrajectory_repr};
