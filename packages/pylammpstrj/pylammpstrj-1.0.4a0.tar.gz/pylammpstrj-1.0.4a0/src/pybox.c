#define PY_SSIZE_T_CLEAN

#include "pybox.h"
#include "box.h"

#include <Python.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <descrobject.h>
#include <floatobject.h>
#include <listobject.h>
#include <object.h>
#include <pymacro.h>
#include <unicodeobject.h>

void PyBox_dealloc(PyBoxObject *self) { Py_TYPE(self)->tp_free((PyObject *) self); }

PyObject *PyBox_new(PyTypeObject *type, PyObject *Py_UNUSED(args), PyObject *Py_UNUSED(kwargs))
{
    PyBoxObject *self;
    self = (PyBoxObject *) type->tp_alloc(type, 0);
    return (PyObject *) self;
}

PyObject *PyBox_get_bounds(PyBoxObject *self, PyObject *Py_UNUSED(closure))
{
    PyObject *list = PyList_New(6);
    for (unsigned int b = 0; b < 6; b++) PyList_SetItem(list, b, PyFloat_FromDouble(self->box.bounds[b]));
    return list;
}

PyObject *PyBox_get_flag(PyBoxObject *self, PyObject *Py_UNUSED(closure)) { return PyUnicode_FromString(self->box.flag); }

PyGetSetDef PyBox_getset[] = {{.name = "bounds", .get = (getter) PyBox_get_bounds, .doc = "The box bounds."},
                              {.name = "flags", .get = (getter) PyBox_get_flag, .doc = "The box flag."},
                              {NULL, NULL, NULL, NULL, NULL}};

PyObject *PyBox_str(PyBoxObject *self)
{
    return PyUnicode_FromFormat("[%S '%s']", PyObject_Str(PyBox_get_bounds(self, NULL)), self->box.flag);
}

PyObject *PyBox_repr(PyBoxObject *self)
{
    return PyUnicode_FromFormat("box(bounds=%S flag='%s')", PyObject_Str(PyBox_get_bounds(self, NULL)), self->box.flag);
}

void PyBox_initialize(PyBoxObject *self, struct Box box) { self->box = box; }

PyTypeObject PyBoxType = {PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pylammpstrj.PyBox",
                          .tp_doc = "Box objects",
                          .tp_basicsize = sizeof(PyBoxObject),
                          .tp_itemsize = 0,
                          .tp_flags = Py_TPFLAGS_DEFAULT,
                          .tp_dealloc = (destructor) PyBox_dealloc,
                          .tp_new = PyBox_new,
                          .tp_getset = PyBox_getset,
                          .tp_str = (reprfunc) PyBox_str,
                          .tp_repr = (reprfunc) PyBox_repr};
