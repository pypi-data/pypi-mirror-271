#ifndef _PYATOM_H
#define _PYATOM_H

#include "atom.h"
#include "pytrajectory.h"

#include <Python.h>

typedef struct PyAtomObject
{
    PyObject_HEAD PyTrajectoryObject *trajectory;
    struct Atom atom;
} PyAtomObject;

PyObject *PyAtom_new(PyTypeObject *type, PyObject *Py_UNUSED(args),
                     PyObject *Py_UNUSED(kwargs));

PyObject *PyAtom_get_id(PyAtomObject *self, void *Py_UNUSED(closure));

PyObject *PyAtom_get_type(PyAtomObject *self, void *Py_UNUSED(closure));

PyObject *PyAtom_get_label(PyAtomObject *self, void *Py_UNUSED(closure));

PyObject *PyAtom_get_x(PyAtomObject *self, void *Py_UNUSED(closure));

PyObject *PyAtom_get_y(PyAtomObject *self, void *Py_UNUSED(closure));

PyObject *PyAtom_get_z(PyAtomObject *self, void *Py_UNUSED(closure));

PyObject *PyAtom_get_charge(PyAtomObject *self, void *Py_UNUSED(closure));

PyObject *PyAtom_get_additional_fields(PyAtomObject *self,
                                       void *Py_UNUSED(closure));

extern PyGetSetDef PyAtom_getset[];

PyObject *PyAtom_str(PyAtomObject *self);

PyObject *PyAtom_repr(PyAtomObject *self);

extern PyTypeObject PyAtomType;

void PyAtom_initialize(PyAtomObject *self, PyTrajectoryObject *trajectory,
                       struct Atom atom);

void PyAtom_dealloc(PyAtomObject *self);

#endif
