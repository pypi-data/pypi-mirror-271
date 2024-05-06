#include <Python.h>
#include <iostream>
#include <exception>
#include <numpy/arrayobject.h>
#include <numpy/ndarrayobject.h>
#include <numpy/npy_common.h>

#include "PersPairExtractor.h"

static char module_docstring[] = "TBA";
static char ppe_docstring[] = "TBA";

static PyObject *extract(PyObject *self, PyObject *args, PyObject *keywds)
{
    import_array();
    Py_Initialize();

    PyObject *input_data_py;

    static char *kwlist[] = {"image", NULL};
    if (!PyArg_ParseTupleAndKeywords(
            args, keywds, "O", kwlist, &input_data_py))
        return NULL;
    std::size_t len = PyArray_SIZE(input_data_py);
    int dimData = PyArray_NDIM(input_data_py);
    npy_intp *dim_array = PyArray_DIMS(input_data_py);

    Triplet triplet;
    if (dimData >= 1)
        triplet.x = dim_array[0];
    if (dimData >= 2)
        triplet.y = dim_array[1];
    if (dimData >= 3)
        triplet.z = dim_array[2];
    input_data_py = PyArray_ContiguousFromAny(input_data_py, NPY_INT32, 0, 0);

    int *PyArrayData = (int *)PyArray_DATA(input_data_py);
    std::vector<PhaseValue> data(len);
    for(std::size_t i = 0; i < len; ++i){
        data[i] = static_cast<PhaseValue>(PyArrayData[i]);
    }

    auto create_empty_numpy_array = []()->PyObject* {
        // Создаем пустой массив
        npy_intp dims[1] = {0}; // размерность массива
        PyObject* pArray = PyArray_SimpleNew(1, dims, NPY_FLOAT); // создаем пустой массив типа double
        return pArray;
    };

    auto fill_array = [create_empty_numpy_array](const std::vector<std::pair<float,float>>& in) -> PyObject*
    {   
        if(in.empty()){
            return create_empty_numpy_array();
        }
        std::vector<float> out(in.size() * 2);
        for (std::size_t i = 0; i < in.size(); ++i)
        {   
            const auto& v = in[i];
            out[2*i] = v.first;
            out[2*i + 1] = v.second;
        }
        npy_intp dims[2] = {in.size(), 2};
        PyObject *array = PyArray_SimpleNew(2, dims, NPY_FLOAT);
        memcpy(PyArray_DATA(array), out.data(), in.size() * 2 * sizeof(float));
        return array;
    };

    auto result = PersPairExtractor::extract(data, triplet);

    auto ar_pd0 = fill_array(result.pd0);
    auto ar_pd1 = fill_array(result.pd1);
    auto ar_pd2 = fill_array(result.pd2);
    
    PyObject *list_result = PyList_New(3);
    PyList_SetItem(list_result, 0, ar_pd0);
    PyList_SetItem(list_result, 1, ar_pd1);
    PyList_SetItem(list_result, 2, ar_pd2);

    return list_result;
}

static void test(PyObject *self, PyObject *args, PyObject *keywds)
{
    return;
}

static PyMethodDef module_methods[] = {
    {"extract", (PyCFunction)extract, METH_VARARGS | METH_KEYWORDS, ppe_docstring},
    {"test", (PyCFunction)test, METH_VARARGS | METH_KEYWORDS, ppe_docstring},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef moduledef = {PyModuleDef_HEAD_INIT, "pyperspairdiamorse",
                                       module_docstring, -1, module_methods};

PyMODINIT_FUNC PyInit_pyperspairdiamorse(void)
{
    Py_Initialize();
    import_array();
    PyObject *module = PyModule_Create(&moduledef);
    if (!module)
    {
        return NULL;
    }
    import_array();
    return module;
}