#include "avideostream.h"

// Bindings for FrameEncoder (Only JPEGEncoder)
static PyObject *JPEGEncoder_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    PyJPEGEncoderObject *self;

    self = (PyJPEGEncoderObject *) type->tp_alloc(type, 0);

    int width, height, quality;

    if (!PyArg_ParseTuple(args, "iii", &width, &height, &quality)) {
        return NULL;
    }

    if (self != NULL) {
        // Handles error freeing by itself.
        if (!createJPEGEncoder(&self->encoder, width, height, quality)) {

            PyErr_SetString(PyExc_RuntimeError, "Failed to create JPEG encoder");
            return NULL;
        }
    }

    return (PyObject *) self;
}

static void JPEGEncoder_dealloc(PyJPEGEncoderObject *self) {
    deinitFrameEncoder(&self->encoder);
    Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyObject *PyJPEGEncoder_convertStreamFrameToJPEGBytes(PyJPEGEncoderObject *self, PyObject *args) {
    PyVideoStreamObject *streamObj;

    if (!PyArg_ParseTuple(args, "O!", &VideoStreamType, &streamObj)) {
        return NULL;
    }

    if (!encodeFrame(&self->encoder, streamObj->stream.frame)) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to encode frame");
        return NULL;
    }

    return Py_BuildValue("y#", self->encoder.packet->data, self->encoder.packet->size);
}

static PyMethodDef JPEGEncoder_methods[] = {
        {"consumeStream", (PyCFunction) PyJPEGEncoder_convertStreamFrameToJPEGBytes, METH_VARARGS, "Convert a frame from a video stream to JPEG bytes"},
        {NULL}
};

static PyTypeObject JPEGEncoderType = {
        PyVarObject_HEAD_INIT(NULL, 0)
        .tp_name = "JPEGEncoder",
        .tp_doc = "JPEG encoder object",
        .tp_basicsize = sizeof(PyJPEGEncoderObject),
        .tp_itemsize = 0,
        .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
        .tp_new = JPEGEncoder_new,
        .tp_dealloc = (destructor) JPEGEncoder_dealloc,
        .tp_methods = JPEGEncoder_methods,
}; // End of bindings for FrameEncoder
// Bindings for VideoStream
static PyObject *VideoStream_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    PyVideoStreamObject *self;

    self = (PyVideoStreamObject *) type->tp_alloc(type, 0);

    const char *uri;

    if (!PyArg_ParseTuple(args, "s", &uri)) {
        return NULL;
    }

    if (self != NULL) {
        // Handles error freeing by itself.
        if (!createVideoStream(&self->stream, uri)) {
            PyErr_SetString(PyExc_RuntimeError, "Failed to create video stream");
            return NULL;
        }
    }

    return (PyObject *) self;
}

static void VideoStream_dealloc(PyVideoStreamObject *self) {
    deinitVideoStream(&self->stream);
    Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyObject *PyVideoStream_dumpInfo(PyVideoStreamObject *self) {
    dumpVideoStreamInfo(&self->stream);
    Py_RETURN_NONE;
}

static PyObject *PyVideoStream_readFrame(PyVideoStreamObject *self) {
    if (!readFrame(&self->stream)) {
        Py_RETURN_FALSE;
    }

    Py_RETURN_TRUE;

}

static PyObject *PyVideoStream_createEncoder(PyVideoStreamObject *self, PyObject *args) {
    int width, height, quality;

    if (!PyArg_ParseTuple(args, "i", &quality)) {
        return NULL;
    }

    width = self->stream.image.width;
    height = self->stream.image.height;

    return PyObject_CallFunction((PyObject *) &JPEGEncoderType, "iii", width, height, quality);
}

static PyMethodDef VideoStream_methods[] = {
        {"dumpInfo",      (PyCFunction) PyVideoStream_dumpInfo,      METH_NOARGS,  "Dump video stream info"},
        {"readFrame",     (PyCFunction) PyVideoStream_readFrame,     METH_NOARGS,  "Read a frame from the video stream"},
        {"createEncoder", (PyCFunction) PyVideoStream_createEncoder, METH_VARARGS, "Create a JPEG encoder for the video stream"},
        {NULL}
};

static PyTypeObject VideoStreamType = {
        PyVarObject_HEAD_INIT(NULL, 0)
        .tp_name = "VideoStream",
        .tp_doc = "Video stream object",
        .tp_basicsize = sizeof(PyVideoStreamObject),
        .tp_itemsize = 0,
        .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
        .tp_new = VideoStream_new,
        .tp_dealloc = (destructor) VideoStream_dealloc,
        .tp_methods = VideoStream_methods,

}; // End of bindings for VideoStream

// Module definition
static PyMethodDef module_methods[] = {
        // Module methods if any
        {NULL}  // Sentinel
};

static struct PyModuleDef module = {
        PyModuleDef_HEAD_INIT,
        .m_name = "avideostream",
        .m_doc = "Directly use libav (ffmpeg) to read RTSP streams with python bindings.",
        .m_size = -1,
        .m_methods = module_methods
};

PyMODINIT_FUNC PyInit_avideostream(void) {
    PyObject * m;

    if (PyType_Ready(&VideoStreamType) < 0) {
        return NULL;
    }

    if (PyType_Ready(&JPEGEncoderType) < 0) {
        return NULL;
    }

    m = PyModule_Create(&module);

    if (m == NULL) {
        return NULL;
    }

    Py_INCREF(&VideoStreamType);
    PyModule_AddObject(m, "VideoStream", (PyObject *) &VideoStreamType);

    Py_INCREF(&JPEGEncoderType);
    PyModule_AddObject(m, "JPEGEncoder", (PyObject *) &JPEGEncoderType);

    return m;
}