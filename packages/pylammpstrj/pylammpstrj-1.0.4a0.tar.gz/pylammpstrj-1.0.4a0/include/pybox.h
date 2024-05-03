#ifndef _PYBOX_H
#define _PYBOX_H

#include "box.h"

#include <Python.h>

typedef struct PyBoxObject
{
    PyObject_HEAD struct Box box;
} PyBoxObject;

void PyBox_dealloc(PyBoxObject *self);

PyObject *PyBox_new(PyTypeObject *type, PyObject *Py_UNUSED(args),
                    PyObject *Py_UNUSED(kwargs));

PyObject *PyBox_get_bounds(PyBoxObject *self, PyObject *Py_UNUSED(closure));

PyObject *PyBox_get_flag(PyBoxObject *self, PyObject *Py_UNUSED(closure));

extern PyGetSetDef PyBox_getset[];

PyObject *PyBox_str(PyBoxObject *self);

PyObject *PyBox_repr(PyBoxObject *self);

void PyBox_initialize(PyBoxObject *self, struct Box box);

extern PyTypeObject PyBoxType;

#endif
