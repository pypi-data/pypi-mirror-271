#define PY_SSIZE_T_CLEAN
#include "pyatom.h"
#include "atom.h"

#include <Python.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <descrobject.h>
#include <floatobject.h>
#include <listobject.h>
#include <longobject.h>
#include <object.h>
#include <pymacro.h>
#include <pytrajectory.h>
#include <unicodeobject.h>

/*
 *  Atom
 */
void PyAtom_dealloc(PyAtomObject *self)
{
    Py_TYPE(self)->tp_free((PyObject *) self);
}

PyObject *PyAtom_new(PyTypeObject *type, PyObject *Py_UNUSED(args), PyObject *Py_UNUSED(kwargs))
{
    PyAtomObject *self;
    self = (PyAtomObject *) type->tp_alloc(type, 0);
    return (PyObject *) self;
}

PyObject *PyAtom_get_id(PyAtomObject *self, void *Py_UNUSED(closure)) { return PyLong_FromUnsignedLong(self->atom.id); }

PyObject *PyAtom_get_type(PyAtomObject *self, void *Py_UNUSED(closure)) { return PyLong_FromUnsignedLong(self->atom.type); }

PyObject *PyAtom_get_label(PyAtomObject *self, void *Py_UNUSED(closure)) { return PyUnicode_FromString(self->atom.label); }

PyObject *PyAtom_get_x(PyAtomObject *self, void *Py_UNUSED(closure)) { return PyFloat_FromDouble(self->atom.position[0]); }

PyObject *PyAtom_get_y(PyAtomObject *self, void *Py_UNUSED(closure)) { return PyFloat_FromDouble(self->atom.position[1]); }

PyObject *PyAtom_get_z(PyAtomObject *self, void *Py_UNUSED(closure)) { return PyFloat_FromDouble(self->atom.position[2]); }

PyObject *PyAtom_get_charge(PyAtomObject *self, void *Py_UNUSED(closure)) { return PyFloat_FromDouble(self->atom.charge); }

PyObject *PyAtom_get_additional_fields(PyAtomObject *self, void *Py_UNUSED(closure))
{
    struct AtomBuilder atom_builder = self->trajectory->trajectory.atom_builder;
    PyObject *list = PyList_New(atom_builder.N_additional);
    for (unsigned int f = 0, f_add = 0; f < atom_builder.N_fields; f++)
    {
        if (!atom_builder.is_additional[f]) continue;
        size_t offset = atom_builder.offsets[f];
        switch (atom_builder.fields_types[f])
        {
            case AFT_INT:
                PyList_SetItem(list, f_add, PyLong_FromLong(self->atom.additionnal_fields[offset].i));
                break;
            case AFT_DOUBLE:
                PyList_SetItem(list, f_add, PyFloat_FromDouble(self->atom.additionnal_fields[offset].d));
                break;
            case AFT_STRING:
                PyList_SetItem(list, f_add, PyUnicode_FromString(self->atom.additionnal_fields[offset].s));
                break;
            default:
                printf("Error: AFT_NULL");
                PyList_SetItem(list, f_add, Py_None);
                break;
        }
        f_add++;
    }

    return (PyObject *) list;
}

PyObject *PyAtom_get_N_bonds(PyAtomObject *self, void *Py_UNUSED(closure)) { return PyLong_FromUnsignedLong(self->atom.N_bonds); }

PyObject *PyAtom_get_total_bo(PyAtomObject *self, void *Py_UNUSED(closure)) { return PyFloat_FromDouble(self->atom.total_bo); }

PyGetSetDef PyAtom_getset[] = {
    {.name = "id", .get = (getter) PyAtom_get_id, .doc = "The ID of the atom."},
    {.name = "type", .get = (getter) PyAtom_get_type, .doc = "The numeric type of the atom."},
    {.name = "label", .get = (getter) PyAtom_get_label, .doc = "The label of the atom (e.g. its element)."},
    {.name = "x", .get = (getter) PyAtom_get_x, .doc = "The x coordinate of the atom."},
    {.name = "y", .get = (getter) PyAtom_get_y, .doc = "The y coordinate of the atom."},
    {.name = "z", .get = (getter) PyAtom_get_z, .doc = "The z coordinate of the atom."},
    {.name = "charge", .get = (getter) PyAtom_get_charge, .doc = "The charge of the atom."},
    {.name = "additional_fields", .get = (getter) PyAtom_get_additional_fields, .doc = "The additional fields of the atom."},
    {.name = "N_bonds", .get = (getter) PyAtom_get_N_bonds, .doc = "The number of bonds of the atom."},
    {.name = "total_bo", .get = (getter) PyAtom_get_total_bo, .doc = "The total bond order of the atom."},
    {0}};

PyObject *PyAtom_str(PyAtomObject *self)
{
    return PyUnicode_FromFormat("[%lu %lu %s %S %S %S %S %S %S %S]", self->atom.id, self->atom.type, self->atom.label,
                                PyObject_Str(PyAtom_get_x(self, NULL)), PyObject_Str(PyAtom_get_y(self, NULL)),
                                PyObject_Str(PyAtom_get_z(self, NULL)), PyObject_Str(PyAtom_get_charge(self, NULL)),
                                PyObject_Str(PyAtom_get_additional_fields(self, NULL)), PyObject_Str(PyAtom_get_N_bonds(self, NULL)),
                                PyObject_Str(PyAtom_get_total_bo(self, NULL)));
}

PyObject *PyAtom_repr(PyAtomObject *self)
{
    return PyUnicode_FromFormat(
        "atom(id=%lu type=%lu label='%s' x=%S y=%S z=%S charge=%S "
        "additional_fields=%S N_bonds=%S totla_bo=%S])",
        self->atom.id, self->atom.type, self->atom.label, PyObject_Str(PyAtom_get_x(self, NULL)), PyObject_Str(PyAtom_get_y(self, NULL)),
        PyObject_Str(PyAtom_get_z(self, NULL)), PyObject_Str(PyAtom_get_charge(self, NULL)),
        PyObject_Str(PyAtom_get_additional_fields(self, NULL)), PyObject_Str(PyAtom_get_N_bonds(self, NULL)),
        PyObject_Str(PyAtom_get_total_bo(self, NULL)));
}

PyTypeObject PyAtomType = {PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pylammpstrj.PyAtom",
                           .tp_doc = "Atom objects",
                           .tp_basicsize = sizeof(PyAtomObject),
                           .tp_itemsize = 0,
                           .tp_flags = Py_TPFLAGS_DEFAULT,
                           .tp_dealloc = (destructor) PyAtom_dealloc,
                           .tp_new = PyAtom_new,
                           .tp_getset = PyAtom_getset,
                           .tp_str = (reprfunc) PyAtom_str,
                           .tp_repr = (reprfunc) PyAtom_repr};

void PyAtom_initialize(PyAtomObject *self, PyTrajectoryObject *trajectory, struct Atom atom)
{
    self->trajectory = trajectory;
    self->atom = atom;
}
