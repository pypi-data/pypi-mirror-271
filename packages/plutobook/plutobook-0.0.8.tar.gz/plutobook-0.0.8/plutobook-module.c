#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>

#include <plutobook.h>

typedef struct {
    PyObject_HEAD
    float width;
    float height;
} PageSize_Object;

static PyObject* PageSize_Create(float width, float height);

static PyObject* PageSize_new(PyTypeObject* type, PyObject* args, PyObject* kwds)
{
    float width= 0, height = 0;
    if(!PyArg_ParseTuple(args, "|ff:PageSize.__init__", &width, &height))
        return NULL;
    Py_ssize_t num_args = PyTuple_Size(args);
    if(num_args == 1) {
        height = width;
    }

    return PageSize_Create(width, height);
}

static void PageSize_dealloc(PageSize_Object* self)
{
    PyObject_Del(self);
}

static PyObject* PageSize_repr(PageSize_Object* self)
{
    char buf[256];
    PyOS_snprintf(buf, sizeof(buf), "plutobook.PageSize(%g, %g)", self->width, self->height);
    return PyUnicode_FromString(buf);
}

static PyMemberDef PageSize_members[] = {
    {"width", T_FLOAT, offsetof(PageSize_Object, width), 0, NULL},
    {"height", T_FLOAT, offsetof(PageSize_Object, height), 0, NULL},
    {NULL}
};

static PyTypeObject PageSize_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "plutobook.PageSize",               /* tp_name */
    sizeof(PageSize_Object),            /* tp_basicsize */
    0,                                  /* tp_itemsize */
    (destructor)PageSize_dealloc,       /* tp_dealloc */
    0,                                  /* tp_print */
    0,                                  /* tp_getattr */
    0,                                  /* tp_setattr */
    0,                                  /* tp_compare */
    (reprfunc)PageSize_repr,            /* tp_repr */
    0,                                  /* tp_as_number */
    0,                                  /* tp_as_sequence */
    0,                                  /* tp_as_mapping */
    0,                                  /* tp_hash */
    0,                                  /* tp_call */
    0,                                  /* tp_str */
    0,                                  /* tp_getattro */
    0,                                  /* tp_setattro */
    0,                                  /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                 /* tp_flags */
    0,                                  /* tp_doc */
    0,                                  /* tp_traverse */
    0,                                  /* tp_clear */
    0,                                  /* tp_richcompare */
    0,                                  /* tp_weaklistoffset */
    0,                                  /* tp_iter */
    0,                                  /* tp_iternext */
    0,                                  /* tp_methods */
    PageSize_members,                   /* tp_members */
    0,                                  /* tp_getset */
    0,                                  /* tp_base */
    0,                                  /* tp_dict */
    0,                                  /* tp_descr_get */
    0,                                  /* tp_descr_set */
    0,                                  /* tp_dictoffset */
    0,                                  /* tp_init */
    0,                                  /* tp_alloc */
    (newfunc)PageSize_new,              /* tp_new */
    0,                                  /* tp_free */
    0,                                  /* tp_is_gc */
    0,                                  /* tp_bases */
};

PyObject* PageSize_Create(float width, float height)
{
    PageSize_Object* size_ob = PyObject_New(PageSize_Object, &PageSize_Type);
    size_ob->width = width;
    size_ob->height = height;
    return (PyObject*)size_ob;
}

typedef struct {
    PyObject_HEAD
    float top;
    float right;
    float bottom;
    float left;
} PageMargins_Object;

static PyObject* PageMargins_Create(float top, float right, float bottom, float left);

static PyObject* PageMargins_new(PyTypeObject* type, PyObject* args, PyObject* kwds)
{
    float top = 0, right = 0, bottom = 0, left = 0;
    if(!PyArg_ParseTuple(args, "|ffff:PageMargins.__init__", &top, &right, &bottom, &left))
        return NULL;
    Py_ssize_t num_args = PyTuple_Size(args);
    if(num_args == 1) {
        right = bottom = left = top;
    } else if(num_args == 2) {
        bottom = top;
        left = right;
    } else if(num_args == 3) {
        left = right;
    }

    return PageMargins_Create(top, right, bottom, left);
}

static void PageMargins_dealloc(PageMargins_Object* self)
{
    PyObject_Del(self);
}

static PyObject* PageMargins_repr(PageMargins_Object* self)
{
    char buf[256];
    PyOS_snprintf(buf, sizeof(buf), "plutobook.PageMargins(%g, %g, %g, %g)", self->top, self->right, self->bottom, self->left);
    return PyUnicode_FromString(buf);
}

static PyMemberDef PageMargins_members[] = {
    {"top", T_FLOAT, offsetof(PageMargins_Object, top), 0, NULL},
    {"right", T_FLOAT, offsetof(PageMargins_Object, right), 0, NULL},
    {"bottom", T_FLOAT, offsetof(PageMargins_Object, bottom), 0, NULL},
    {"left", T_FLOAT, offsetof(PageMargins_Object, left), 0, NULL},
    {NULL}
};

static PyTypeObject PageMargins_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "plutobook.PageMargins",            /* tp_name */
    sizeof(PageMargins_Object),         /* tp_basicsize */
    0,                                  /* tp_itemsize */
    (destructor)PageMargins_dealloc,    /* tp_dealloc */
    0,                                  /* tp_print */
    0,                                  /* tp_getattr */
    0,                                  /* tp_setattr */
    0,                                  /* tp_compare */
    (reprfunc)PageMargins_repr,         /* tp_repr */
    0,                                  /* tp_as_number */
    0,                                  /* tp_as_sequence */
    0,                                  /* tp_as_mapping */
    0,                                  /* tp_hash */
    0,                                  /* tp_call */
    0,                                  /* tp_str */
    0,                                  /* tp_getattro */
    0,                                  /* tp_setattro */
    0,                                  /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                 /* tp_flags */
    0,                                  /* tp_doc */
    0,                                  /* tp_traverse */
    0,                                  /* tp_clear */
    0,                                  /* tp_richcompare */
    0,                                  /* tp_weaklistoffset */
    0,                                  /* tp_iter */
    0,                                  /* tp_iternext */
    0,                                  /* tp_methods */
    PageMargins_members,                /* tp_members */
    0,                                  /* tp_getset */
    0,                                  /* tp_base */
    0,                                  /* tp_dict */
    0,                                  /* tp_descr_get */
    0,                                  /* tp_descr_set */
    0,                                  /* tp_dictoffset */
    0,                                  /* tp_init */
    0,                                  /* tp_alloc */
    (newfunc)PageMargins_new,           /* tp_new */
    0,                                  /* tp_free */
    0,                                  /* tp_is_gc */
    0,                                  /* tp_bases */
};

PyObject* PageMargins_Create(float top, float right, float bottom, float left)
{
    PageMargins_Object* margins_ob = PyObject_New(PageMargins_Object, &PageMargins_Type);
    margins_ob->top = top;
    margins_ob->right = right;
    margins_ob->bottom = bottom;
    margins_ob->left = left;
    return (PyObject*)margins_ob;
}

typedef struct {
    PyObject_HEAD
    plutobook_t* book;
} Book_Object;

static PyObject* Book_new(PyTypeObject* type, PyObject* args, PyObject* kwds)
{
    static char* kwlist[] = { "size", "margins", "media", NULL };
    PageSize_Object* size_ob = NULL;
    PageMargins_Object* margins_ob = NULL;
    plutobook_media_type_t media_type = PLUTOBOOK_MEDIA_TYPE_PRINT;
    if(!PyArg_ParseTupleAndKeywords(args, kwds, "|O!O!i:Book.__init__", kwlist, &PageSize_Type, &size_ob, &PageMargins_Type, &margins_ob, &media_type)) {
        return NULL;
    }

    plutobook_page_size_t size = PLUTOBOOK_PAGE_SIZE_A4;
    if(size_ob) {
        size.width = size_ob->width;
        size.height = size_ob->height;
    }

    plutobook_page_margins_t margins = PLUTOBOOK_PAGE_MARGINS_NORMAL;
    if(margins_ob) {
        margins.top = margins_ob->top;
        margins.right = margins_ob->right;
        margins.bottom = margins_ob->bottom;
        margins.left = margins_ob->left;
    }

    plutobook_t* book = plutobook_create(size, margins, media_type);
    if(book == NULL)
        return NULL;
    Book_Object* book_ob = PyObject_New(Book_Object, type);
    book_ob->book = book;
    return (PyObject*)book_ob;
}

static void Book_dealloc(Book_Object* self)
{
    plutobook_destroy(self->book);
    PyObject_Del(self);
}

static PyObject* Book_get_viewport_width(Book_Object* self, PyObject* args)
{
    return Py_BuildValue("f", plutobook_get_viewport_width(self->book));
}

static PyObject* Book_get_viewport_height(Book_Object* self, PyObject* args)
{
    return Py_BuildValue("f", plutobook_get_viewport_height(self->book));
}

static PyObject* Book_get_document_width(Book_Object* self, PyObject* args)
{
    float document_width;
    Py_BEGIN_ALLOW_THREADS
    document_width = plutobook_get_document_width(self->book);
    Py_END_ALLOW_THREADS
    return Py_BuildValue("f", document_width);
}

static PyObject* Book_get_document_height(Book_Object* self, PyObject* args)
{
    float document_height;
    Py_BEGIN_ALLOW_THREADS
    document_height = plutobook_get_document_height(self->book);
    Py_END_ALLOW_THREADS
    return Py_BuildValue("f", document_height);
}

static PyObject* Book_get_page_count(Book_Object* self, PyObject* args)
{
    int page_count;
    Py_BEGIN_ALLOW_THREADS
    page_count = plutobook_get_page_count(self->book);
    Py_END_ALLOW_THREADS
    return PyLong_FromLong(page_count);
}

static PyMethodDef Book_methods[] = {
    {"get_viewport_width", (PyCFunction)Book_get_viewport_width, METH_NOARGS},
    {"get_viewport_height", (PyCFunction)Book_get_viewport_height, METH_NOARGS},
    {"get_document_width", (PyCFunction)Book_get_document_width, METH_NOARGS},
    {"get_document_height", (PyCFunction)Book_get_document_height, METH_NOARGS},
    {"get_page_count", (PyCFunction)Book_get_page_count, METH_NOARGS},
    {NULL}
};

static PyTypeObject Book_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "plutobook.Book",                   /* tp_name */
    sizeof(Book_Object),                /* tp_basicsize */
    0,                                  /* tp_itemsize */
    (destructor)Book_dealloc,           /* tp_dealloc */
    0,                                  /* tp_print */
    0,                                  /* tp_getattr */
    0,                                  /* tp_setattr */
    0,                                  /* tp_compare */
    0,                                  /* tp_repr */
    0,                                  /* tp_as_number */
    0,                                  /* tp_as_sequence */
    0,                                  /* tp_as_mapping */
    0,                                  /* tp_hash */
    0,                                  /* tp_call */
    0,                                  /* tp_str */
    0,                                  /* tp_getattro */
    0,                                  /* tp_setattro */
    0,                                  /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                 /* tp_flags */
    0,                                  /* tp_doc */
    0,                                  /* tp_traverse */
    0,                                  /* tp_clear */
    0,                                  /* tp_richcompare */
    0,                                  /* tp_weaklistoffset */
    0,                                  /* tp_iter */
    0,                                  /* tp_iternext */
    Book_methods,                       /* tp_methods */
    0,                                  /* tp_members */
    0,                                  /* tp_getset */
    0,                                  /* tp_base */
    0,                                  /* tp_dict */
    0,                                  /* tp_descr_get */
    0,                                  /* tp_descr_set */
    0,                                  /* tp_dictoffset */
    0,                                  /* tp_init */
    0,                                  /* tp_alloc */
    (newfunc)Book_new,                  /* tp_new */
    0,                                  /* tp_free */
    0,                                  /* tp_is_gc */
    0,                                  /* tp_bases */
};

static PyObject* module_version(PyObject* self, PyObject* args)
{
    return PyLong_FromLong(plutobook_version());
}

static PyObject* module_version_string(PyObject* self, PyObject* args)
{
    return PyUnicode_FromString(plutobook_version_string());
}

static PyMethodDef module_methods[] = {
    {"version", (PyCFunction)module_version, METH_NOARGS},
    {"version_string", (PyCFunction)module_version_string, METH_NOARGS},
    {NULL},
};

static struct PyModuleDef module_definition = {
    PyModuleDef_HEAD_INIT,
    "plutobook",
    0,
    0,
    module_methods,
    0,
    0,
    0,
    0,
};

PyMODINIT_FUNC PyInit_plutobook(void)
{
    if(PyType_Ready(&PageSize_Type) < 0)
        return NULL;
    if(PyType_Ready(&PageMargins_Type) < 0)
        return NULL;
    if(PyType_Ready(&Book_Type) < 0)
        return NULL;
    PyObject* module = PyModule_Create(&module_definition);
    if(module == NULL)
        return NULL;
    Py_INCREF(&PageSize_Type);
    Py_INCREF(&PageMargins_Type);
    Py_INCREF(&Book_Type);

    PyModule_AddObject(module, "PageSize", (PyObject*)&PageSize_Type);
    PyModule_AddObject(module, "PageMargins", (PyObject*)&PageMargins_Type);
    PyModule_AddObject(module, "Book", (PyObject*)&Book_Type);
    return module;
}
