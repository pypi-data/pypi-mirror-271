#ifndef PYLAMMPSTRJMODULE_H
#define PYLAMMPSTRJMODULE_H

#include <Python.h>

PyObject *pylammpstrj_read(PyObject *Py_UNUSED(self), PyObject *args,
                                  PyObject *kwds);

extern PyMethodDef pylammpstrj_methods[];

extern struct PyModuleDef pylammpstrjmodule;

#endif
