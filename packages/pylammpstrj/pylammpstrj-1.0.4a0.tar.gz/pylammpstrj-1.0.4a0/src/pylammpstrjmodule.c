#include "select.h"
#define PY_SSIZE_T_CLEAN

#include "pylammpstrjmodule.h"
#include "bond.h"
#include "pyatom.h"
#include "pybox.h"
#include "pytrajectory.h"
#include "trajectory.h"
#include "utils.h"

#include <errno.h>
#include <Python.h>
#include <stdio.h>

#include <bytesobject.h>
#include <methodobject.h>
#include <modsupport.h>
#include <moduleobject.h>
#include <object.h>
#include <pyerrors.h>
#include <pymacro.h>
#include <pyport.h>
#include <unicodeobject.h>

PyObject *pylammpstrj_read(PyObject *Py_UNUSED(self), PyObject *args, PyObject *kwargs)
{
    char *kwlist[] = {"", "start", "delay", "batch_size", NULL};
    PyObject *bytes;
    Py_ssize_t length;
    char *file_name;
    unsigned long start = 0;
    int delay = 0;
    unsigned int batch_size = 100;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O&|$ipi", kwlist, PyUnicode_FSConverter, &bytes, &start, &delay, &batch_size))
        return NULL;

    PyBytes_AsStringAndSize(bytes, &file_name, &length);
    if (length > FILE_NAME_LIMIT)
    {
        PyErr_SetString(PyExc_RuntimeError, "File name too long (PyTrajectory.read_bonds)");
        Py_DECREF(bytes);
        return NULL;
    }

    // Initializing
    if (delay)
    {
        PyTrajectoryFileObject *pytrajectory_file = (PyTrajectoryFileObject *) PyTrajectoryFile_new(&PyTrajectoryFileType, NULL, NULL);
        if (pytrajectory_file == NULL)
        {
            Py_DECREF(bytes);
            return NULL;
        }

        struct TrajectoryFile trajectory_file = trajectoryfile_new(file_name, NULL, batch_size);
        if (errno != 0)
        {
            PyTrajectoryFileType.tp_free((PyObject *) pytrajectory_file);
            Py_DECREF(bytes);
            perror("Error while creating the TrajectoryFile (pylammpstrj_read.trajectory_file)");
            return PyErr_SetFromErrno(PyExc_RuntimeError);
        }

        PyTrajectoryFile_initialize(pytrajectory_file, trajectory_file);
        Py_DECREF(bytes);
        return (PyObject *) pytrajectory_file;
    }

    PyTrajectoryObject *pytrajectory = (PyTrajectoryObject *) PyTrajectory_new(&PyTrajectoryType, NULL, NULL);
    if (pytrajectory == NULL)
    {
        Py_DECREF(bytes);
        return NULL;
    }

    struct Trajectory trajectory;
    trajectory_read(file_name, start, NULL, &trajectory);
    if (errno != 0)
    {
        PyTrajectoryType.tp_free((PyObject *) pytrajectory);
        Py_DECREF(bytes);
        perror("Error while reading the trajectory (pylammpstrj_read.trajectory)");
        return PyErr_SetFromErrno(PyExc_RuntimeError);
    }

    PyTrajectory_initialize(pytrajectory, trajectory);
    Py_DECREF(bytes);
    return (PyObject *) pytrajectory;
}

PyMethodDef pylammpstrj_methods[] = {
    {"read", (PyCFunction) (void (*)(void)) pylammpstrj_read, METH_VARARGS | METH_KEYWORDS, "Read a trajectory file."}, {0}};

struct PyModuleDef pylammpstrjmodule = {.m_base = PyModuleDef_HEAD_INIT,
                                        .m_name = "pylammpstrj",
                                        .m_doc = "A module to read and process LAMMPS trajectory files.",
                                        .m_size = -1,
                                        .m_methods = pylammpstrj_methods};

PyMODINIT_FUNC PyInit_pylammpstrj(void)
{
    PyObject *m;

    if (PyType_Ready(&PyAtomType) < 0) return NULL;
    if (PyType_Ready(&PyBoxType) < 0) return NULL;
    if (PyType_Ready(&PyTrajectoryType) < 0) return NULL;
    if (PyType_Ready(&PyTrajectoryFileType) < 0) return NULL;

    m = PyModule_Create(&pylammpstrjmodule);
    if (m == NULL) return NULL;

    Py_INCREF(&PyAtomType);
    if (PyModule_AddObject(m, "PyAtom", (PyObject *) &PyAtomType) < 0)
    {
        Py_XDECREF(&PyAtomType);
        Py_XDECREF(&m);
        return NULL;
    }

    Py_INCREF(&PyBoxType);
    if (PyModule_AddObject(m, "PyBox", (PyObject *) &PyBoxType) < 0)
    {
        Py_XDECREF(&PyBoxType);
        Py_XDECREF(&PyAtomType);
        Py_XDECREF(&m);
        return NULL;
    }

    Py_INCREF(&PyTrajectoryType);
    if (PyModule_AddObject(m, "PyTrajectory", (PyObject *) &PyTrajectoryType) < 0)
    {
        Py_XDECREF(&PyTrajectoryType);
        Py_XDECREF(&PyBoxType);
        Py_XDECREF(&PyAtomType);
        Py_XDECREF(&m);
        return NULL;
    }

    Py_INCREF(&PyTrajectoryFileType);
    if (PyModule_AddObject(m, "PyTrajectoryFile", (PyObject *) &PyTrajectoryFileType) < 0)
    {
        Py_XDECREF(&PyTrajectoryFileType);
        Py_XDECREF(&PyTrajectoryType);
        Py_XDECREF(&PyBoxType);
        Py_XDECREF(&PyAtomType);
        Py_XDECREF(&m);
        return NULL;
    }

    // Module constants
    PyModule_AddIntConstant(m, "LESS_THAN", (long) OPERATOR_LT);
    PyModule_AddIntConstant(m, "LESS_THAN_EQUAL_TO", (long) OPERATOR_LEQ);
    PyModule_AddIntConstant(m, "EQUAL_TO", (long) OPERATOR_EQ);
    PyModule_AddIntConstant(m, "GREATER_THAN_EQUAL_TO", (long) OPERATOR_GEQ);
    PyModule_AddIntConstant(m, "GREATER_THAN", (long) OPERATOR_GT);
    PyModule_AddIntConstant(m, "BOND_MODE_NULL", (long) BM_NULL);
    PyModule_AddIntConstant(m, "BOND_MODE_ID", (long) BM_ID);
    PyModule_AddIntConstant(m, "BOND_MODE_BOND_ORDER", (long) BM_BOND_ORDER);
    PyModule_AddIntConstant(m, "BOND_MODE_FULL", (long) BM_FULL);
    // PyModule_AddIntConstant(m, "BOND_SELECTION_N_BONDS", (long) BS_N_BONDS);
    // PyModule_AddIntConstant(m, "BOND_SELECTION_TOTAL_BOND_ORDER", (long) BS_TOTAL_BO);

    return m;
}
