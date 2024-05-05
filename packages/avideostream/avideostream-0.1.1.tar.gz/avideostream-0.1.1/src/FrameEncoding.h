#pragma once

#include <libavcodec/avcodec.h>
#include <libavutil/imgutils.h>
#include <stdbool.h>

#include "Utils.h"

typedef struct {
    // Contains response data
    AVPacket *packet;

    // Decoder context
    AVCodecContext *codecCtx;
    const AVCodec *codec;
} FrameEncoder;

bool initFrameEncoder(FrameEncoder *encoder, enum AVCodecID codecId);

void deinitFrameEncoder(FrameEncoder *encoder);

bool openEncoder(FrameEncoder *encoder);

bool encodeFrame(FrameEncoder *encoder, AVFrame *frame);

bool createJPEGEncoder(FrameEncoder *encoder, int width, int height, int quality);

bool writeEncoderPacketToFile(FrameEncoder *encoder, const char *filename);