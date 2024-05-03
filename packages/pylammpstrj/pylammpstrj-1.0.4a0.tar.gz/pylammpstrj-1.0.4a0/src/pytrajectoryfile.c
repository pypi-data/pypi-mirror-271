#define PY_SSIZE_T_CLEAN

#include "pytrajectory.h"
#include "select.h"
#include "trajectory.h"

#include <errno.h>
#include <Python.h>
#include <stdio.h>
#include <stdlib.h>

#include <descrobject.h>
#include <floatobject.h>
#include <listobject.h>
#include <longobject.h>
#include <methodobject.h>
#include <modsupport.h>
#include <object.h>
#include <pyerrors.h>
#include <pymacro.h>
#include <pyutils.h>
#include <unicodeobject.h>

PyObject *PyTrajectoryFile_new(PyTypeObject *type, PyObject *Py_UNUSED(args), PyObject *Py_UNUSED(kwargs))
{
    PyTrajectoryFileObject *self;
    self = (PyTrajectoryFileObject *) type->tp_alloc(type, 0);
    return (PyObject *) self;
}

void PyTrajectoryFile_initialize(PyTrajectoryFileObject *self, const struct TrajectoryFile trajectory_file)
{
    self->trajectory_file = trajectory_file;
}

void PyTrajectoryFile_dealloc(PyTrajectoryFileObject *self)
{
    trajectoryfile_delete(&(self->trajectory_file));
    PyTrajectoryFileType.tp_free((PyObject *) self);
}

PyObject *PyTrajectoryFile_str(PyTrajectoryFileObject *self)
{
    return PyUnicode_FromFormat("%S %s %S", PyObject_Str(PyTrajectoryFile_get_N_configurations(self, NULL)),
                                PyTrajectoryFile_get_file_name(self, NULL), PyObject_Str(PyTrajectoryFile_get_batch_size(self, NULL)));
}

PyObject *PyTrajectoryFile_repr(PyTrajectoryFileObject *self)
{
    return PyUnicode_FromFormat("trajectoryfile(N_configuration=%S file_name=%s batch_size=%S)",
                                PyObject_Str(PyTrajectoryFile_get_N_configurations(self, NULL)), PyTrajectoryFile_get_file_name(self, NULL),
                                PyObject_Str(PyTrajectoryFile_get_batch_size(self, NULL)));
}

PyObject *PyTrajectoryFile_get_N_configurations(PyTrajectoryFileObject *self, PyObject *Py_UNUSED(closure))
{
    return PyLong_FromLong(self->trajectory_file.N_configurations);
}

PyObject *PyTrajectoryFile_get_steps(PyTrajectoryFileObject *self, PyObject *Py_UNUSED(closure))
{
    PyObject *list = PyList_New(self->trajectory_file.N_configurations);
    if (list == NULL) return NULL;

    for (unsigned int c = 0; c < self->trajectory_file.N_configurations; c++)
        PyList_SetItem(list, c, PyLong_FromLong(self->trajectory_file.steps[c]));

    return list;
}

PyObject *PyTrajectoryFile_get_file_name(PyTrajectoryFileObject *self, PyObject *Py_UNUSED(closure))
{
    return PyUnicode_FromString(self->trajectory_file.file_name);
}

PyObject *PyTrajectoryFile_get_batch_size(PyTrajectoryFileObject *self, PyObject *Py_UNUSED(closure))
{
    return PyLong_FromLong(self->trajectory_file.batch_size);
}

PyGetSetDef PyTrajectoryFile_getset[] = {
    {.name = "N_configurations", .get = (getter) PyTrajectoryFile_get_N_configurations, .doc = "The number of configurations."},
    {.name = "steps", .get = (getter) PyTrajectoryFile_get_steps, .doc = "The timesteps."},
    {.name = "file_name", .get = (getter) PyTrajectoryFile_get_file_name, .doc = "The name of the trajectory file."},
    {.name = "batch_size", .get = (getter) PyTrajectoryFile_get_batch_size, .doc = "The size of the batches."},
    {0}};

PyObject *PyTrajectoryFile_select(PyTrajectoryFileObject *self, PyObject *args)
{
    unsigned int field = 0;
    enum Operator op = 0;
    union SelectionValue value = {0};
    char *field_name = NULL;
    long input_op = 0;
    PyObject *input_value = NULL;
    enum SelectionType type = 0;

    if (!PyArg_ParseTuple(args, "siO", &field_name, &input_op, &input_value))  // Could not parse the arguments
    {
        PyErr_SetString(PyExc_RuntimeError, "Could not parse the arguments");
        return NULL;
    }

    struct Trajectory tmp;
    trajectoryfile_read_slice(self->trajectory_file, 0, 1, &tmp);
    if (errno != 0)  // Could not read trajectory file
    {
        perror("Error while reading the trajectory file");
        PyErr_SetFromErrno(PyExc_RuntimeError);
        return NULL;
    }

    field = parse_field_name(tmp.atom_builder, field_name, &type);
    if (PyErr_Occurred()) return NULL;

    op = parse_operator(input_op);
    if (PyErr_Occurred()) return NULL;

    value = parse_selection_value(type, tmp.atom_builder, field, input_value);
    if (PyErr_Occurred()) return NULL;

    trajectory_delete(&tmp);

    trajectoryfile_select_atoms(&(self->trajectory_file), (struct Selection){.type = type, .field = field, .op = op, .value = value});
    if (errno != 0)  // Could not select atoms
    {
        perror("Error while selecting the atoms");
        PyErr_SetFromErrno(PyExc_RuntimeError);
        return NULL;
    }

    Py_RETURN_NONE;
}

PyObject *PyTrajectoryFile_compute_average(PyTrajectoryFileObject *self, PyObject *args)
{
    char *field_name;
    if (!PyArg_ParseTuple(args, "s", &field_name)) return NULL;

    struct Trajectory tmp;
    trajectoryfile_read_slice(self->trajectory_file, 0, 1, &tmp);
    if (errno != 0)  // Could not read the trajectory file
    {
        perror("Error while reading the trajectory file");
        PyErr_SetFromErrno(PyExc_RuntimeError);
        return NULL;
    }

    // Converting the field name
    enum SelectionType type = 0;
    unsigned int field = parse_field_name(tmp.atom_builder, field_name, &type);
    trajectory_delete(&tmp);

    if (PyErr_Occurred()) return NULL;

    double *averages = trajectoryfile_average_property(self->trajectory_file, field);
    PyObject *list = PyList_New(self->trajectory_file.N_configurations);
    if (list == NULL)
    {
        free(averages);
        return NULL;
    }

    for (unsigned int c = 0; c < self->trajectory_file.N_configurations; c++) PyList_SetItem(list, c, PyFloat_FromDouble(averages[c]));

    free(averages);
    return list;
}

PyObject *PyTrajectoryFile_load(PyTrajectoryFileObject *self)
{
    PyTrajectoryObject *pytrajectory = (PyTrajectoryObject *) PyTrajectory_new(&PyTrajectoryType, NULL, NULL);

    struct Trajectory trajectory;
    trajectoryfile_read_slice(self->trajectory_file, 0, self->trajectory_file.N_configurations, &trajectory);
    if (errno != 0)  // Could not read trajectory file
    {
        perror("Error while reading the trajectory file");
        PyErr_SetFromErrno(PyExc_RuntimeError);
        return NULL;
    }

    PyTrajectory_initialize(pytrajectory, trajectory);
    return (PyObject *) pytrajectory;
}

PyMethodDef PyTrajectoryFile_methods[] = {
    {"select", (PyCFunction) (void (*)(void)) PyTrajectoryFile_select, METH_VARARGS | METH_KEYWORDS, "Store selection parameters."},
    {"compute_average", (PyCFunction) PyTrajectoryFile_compute_average, METH_VARARGS, "Computes average of property over the atoms."},
    {"load", (PyCFunction) (void (*)(void)) PyTrajectoryFile_load, METH_NOARGS,
     "Loads a pylammpstrj.PyTrajectory from a pylammpstrj.PyTrajectoryFile."},
    {0}};

PyTypeObject PyTrajectoryFileType = {PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pylammpstrj.PyTrajectoryFile",
                                     .tp_doc = "Trajectory file object",
                                     .tp_basicsize = sizeof(PyTrajectoryFileObject),
                                     .tp_itemsize = 0,
                                     .tp_flags = Py_TPFLAGS_DEFAULT,
                                     .tp_dealloc = (destructor) PyTrajectoryFile_dealloc,
                                     .tp_new = PyTrajectoryFile_new,
                                     .tp_getset = PyTrajectoryFile_getset,
                                     .tp_methods = PyTrajectoryFile_methods,
                                     .tp_str = (reprfunc) PyTrajectoryFile_str,
                                     .tp_repr = (reprfunc) PyTrajectoryFile_repr};
