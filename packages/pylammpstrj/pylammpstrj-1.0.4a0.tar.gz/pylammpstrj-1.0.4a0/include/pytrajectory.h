#ifndef _PYTRAJECTORY_H
#define _PYTRAJECTORY_H

#include "trajectory.h"

#include <Python.h>
#include <stdbool.h>

#include <descrobject.h>
#include <methodobject.h>
#include <object.h>
#include <pymacro.h>

typedef struct PyTrajectoryObject
{
    PyObject_HEAD struct Trajectory trajectory;
} PyTrajectoryObject;

void PyTrajectory_dealloc(PyTrajectoryObject *self);

PyObject *PyTrajectory_new(PyTypeObject *type, PyObject *Py_UNUSED(args), PyObject *Py_UNUSED(kwargs));

PyObject *PyTrajectory_get_N_configurations(PyTrajectoryObject *self, void *Py_UNUSED(closure));

PyObject *PyTrajectory_get_steps(PyTrajectoryObject *self, void *Py_UNUSED(closure));

PyObject *PyTrajectory_get_N_atoms(PyTrajectoryObject *self, void *Py_UNUSED(closure));

PyObject *PyTrajectory_get_dump_format(PyTrajectoryObject *self, void *Py_UNUSED(closure));

PyObject *PyTrajectory_get_field_names(PyTrajectoryObject *self, void *Py_UNUSED(closure));

PyObject *PyTrajectory_get_additional_fields(PyTrajectoryObject *self, void *Py_UNUSED(closure));

PyObject *PyTrajectory_get_atoms(PyTrajectoryObject *self, void *Py_UNUSED(closure));

PyObject *PyTrajectory_get_boxes(PyTrajectoryObject *self, void *Py_UNUSED(closure));

PyObject *PyTrajectory_get_bond_mode(PyTrajectoryObject *self, void *Py_UNUSED(closure));

extern PyGetSetDef PyTrajectory_getset[];

PyObject *PyTrajectory_str(PyTrajectoryObject *self);

PyObject *PyTrajectory_repr(PyTrajectoryObject *self);

void PyTrajectory_initialize(PyTrajectoryObject *self, struct Trajectory trajectory);

PyObject *PyTrajectory_select(PyTrajectoryObject *self, PyObject *args, PyObject *kwargs);

PyObject *PyTrajectory_moving_select(PyTrajectoryObject *self, PyObject *args, PyObject *kwargs);

PyObject *PyTrajectory_compute_bonds(PyTrajectoryObject *self, PyObject *args);

PyObject *PyTrajectory_compute_average(PyTrajectoryObject *self, PyObject *args);

extern PyMethodDef PyTrajectory_methods[];

extern PyTypeObject PyTrajectoryType;

typedef struct PyTrajectoryFileObject
{
    PyObject_HEAD struct TrajectoryFile trajectory_file;
} PyTrajectoryFileObject;

PyObject *PyTrajectoryFile_new(PyTypeObject *type, PyObject *Py_UNUSED(args), PyObject *Py_UNUSED(kwargs));

void PyTrajectoryFile_initialize(PyTrajectoryFileObject *self, const struct TrajectoryFile trajectory_file);

void PyTrajectoryFile_dealloc(PyTrajectoryFileObject *self);

PyObject *PyTrajectoryFile_str(PyTrajectoryFileObject *self);

PyObject *PyTrajectoryFile_repr(PyTrajectoryFileObject *self);

PyObject *PyTrajectoryFile_get_N_configurations(PyTrajectoryFileObject *self, PyObject *Py_UNUSED(closure));

PyObject *PyTrajectoryFile_get_steps(PyTrajectoryFileObject *self, PyObject *Py_UNUSED(closure));

PyObject *PyTrajectoryFile_get_file_name(PyTrajectoryFileObject *self, PyObject *Py_UNUSED(closure));

PyObject *PyTrajectoryFile_get_batch_size(PyTrajectoryFileObject *self, PyObject *Py_UNUSED(closure));

PyObject *PyTrajectoryFile_get_selections(PyTrajectoryFileObject *self, PyObject *Py_UNUSED(closure));

extern PyGetSetDef PyTrajectoryFile_getset[];

PyObject *PyTrajectory_select(PyTrajectoryObject *self, PyObject *args, PyObject *kwargs);

PyObject *PyTrajectoryFile_compute_average(PyTrajectoryFileObject *self, PyObject *args);

PyObject *PyTrajectoryFile_load(PyTrajectoryFileObject *self);

extern PyMethodDef PyTrajectoryFile_methods[];

extern PyTypeObject PyTrajectoryFileType;

#endif
