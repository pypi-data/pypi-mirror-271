#include <Python.h>

#include <plutobook/plutobook.h>

static PyObject* foo(PyObject* self)
{
    plutobook_t* book = plutobook_create(PLUTOBOOK_PAGE_SIZE_A4, PLUTOBOOK_PAGE_MARGINS_NORMAL, PLUTOBOOK_MEDIA_TYPE_PRINT);
    plutobook_load_html(book, "<b> Hello World </b>", -1, "", "", "");
    plutobook_write_to_pdf(book, "hello.pdf");
    plutobook_destroy(book);
    return PyUnicode_FromString("bar");
}

static PyMethodDef methods[] = {
    {"foo", (PyCFunction)foo, METH_NOARGS, NULL},
    {NULL, NULL, 0, NULL},
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "plutobook",
    NULL,
    -1,
    methods,
};

PyMODINIT_FUNC PyInit_plutobook(void)
{
    return PyModule_Create(&module);
}
