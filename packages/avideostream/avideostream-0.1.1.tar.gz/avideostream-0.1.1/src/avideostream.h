#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include "VideoStream.h"
#include "FrameEncoding.h"

typedef struct {
    PyObject_HEAD
    AVFrame *frame;
} PyAVFrameObject;

typedef struct {
    PyObject_HEAD
    VideoStream stream;
} PyVideoStreamObject;


typedef struct {
    PyObject_HEAD
    FrameEncoder encoder;
} PyJPEGEncoderObject;

static PyTypeObject VideoStreamType;
static PyTypeObject JPEGEncoderType;
