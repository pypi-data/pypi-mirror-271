#pragma once

#include <libavformat/avformat.h>
#include <libavcodec/avcodec.h>
#include <stdbool.h>

#include "Utils.h"


// Holds previous image data
typedef struct {
    unsigned char *data;
    int step;
    int width;
    int height;
} Image;

typedef struct {
    const char *uri;

    AVFormatContext *fmtCtx;
    AVPacket packet;
    AVFrame *frame;
    Image image;

    uint64_t frameNumber;
    int videoStreamIndex;

    AVCodecParameters *codecParams;
    AVCodecContext *codecCtx;
} VideoStream;

void initVideoStream(VideoStream *stream, const char *uri);

void deinitVideoStream(VideoStream *stream);

bool openVideoStream(VideoStream *stream);

bool createVideoStream(VideoStream *stream, const char *uri);

bool readFrame(VideoStream *stream);

void dumpVideoStreamInfo(VideoStream *stream);
