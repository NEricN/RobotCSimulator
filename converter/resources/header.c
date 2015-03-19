#include <Python.h>
#include <Windows.h>
PyObject *pName, *pModule, *pDict, *pInit, *pDeInit,
         *pMotorFunc, *pGetEncoderFunc, *pSetEncoderFunc, *pGetSensorFunc;
void initPython()
{
    Py_Initialize();

    pName = PyString_FromString("vrepAbstractor");
    pModule = PyImport_Import(pName);

    pDict = PyModule_GetDict(pModule); // all these functions

    pMotorFunc = PyDict_GetItemString(pDict, "set_motor");
    pGetEncoderFunc = PyDict_GetItemString(pDict, "get_encoder");
    pSetEncoderFunc = PyDict_GetItemString(pDict, "set_encoder");
    pGetSensorFunc = PyDict_GetItemString(pDict, "get_sensor");
    pInit = PyDict_GetItemString(pDict, "init");
    pDeInit = PyDict_GetItemString(pDict, "de_init");

    PyObject_CallObject(pInit, NULL);
}

void deInitPython()
{
    PyObject_CallObject(pDeInit, NULL);

    Py_DECREF(pModule);
    Py_DECREF(pName);
    Py_Finalize();
}

void driveMotor(int motor, int speed)
{
    PyObject *pArgs = PyTuple_New(2);
    PyTuple_SetItem(pArgs, 0, PyInt_FromLong(motor));
    PyTuple_SetItem(pArgs, 1, PyInt_FromLong(speed));

    PyObject_CallObject(pMotorFunc, pArgs);

    if(pArgs != NULL) {
        Py_DECREF(pArgs);
    }
}

void setEncoder(int encoder, int value)
{
    PyObject *pArgs = PyTuple_New(2);
    PyTuple_SetItem(pArgs, 0, PyInt_FromLong(encoder));
    PyTuple_SetItem(pArgs, 1, PyInt_FromLong(value));

    PyObject_CallObject(pSetEncoderFunc, pArgs);

    if(pArgs != NULL) {
        Py_DECREF(pArgs);
    }
}

int getEncoder(int encoder)
{
    PyObject *pArgs = PyTuple_New(1);
    PyTuple_SetItem(pArgs, 0, PyInt_FromLong(encoder));

    int result = PyFloat_AsDouble(PyObject_CallObject(pGetEncoderFunc, pArgs));

    if(pArgs != NULL) {
        Py_DECREF(pArgs);
    }

    return result;
}

int getSensor(int sensor)
{
    PyObject *pArgs = PyTuple_New(1);
    PyTuple_SetItem(pArgs, 0, PyInt_FromLong(sensor));

    int result = PyFloat_AsDouble(PyObject_CallObject(pGetSensorFunc, pArgs));

    if(pArgs != NULL) {
        Py_DECREF(pArgs);
    }

    return result;
}

void printSensorValue(int sensor)
{
    printf("%d\n", getSensor(sensor));
}

void print(const char *str)
{
    printf(str);
}
