#include "FrameEncoding.h"

bool initFrameEncoder(FrameEncoder *encoder, enum AVCodecID codecId) {
    encoder->codec = avcodec_find_encoder(codecId);

    if (!encoder->codec) {
        LOG("Codec not found\n")
        return false;
    }

    encoder->codecCtx = avcodec_alloc_context3(encoder->codec);

    if (!encoder->codecCtx) {
        LOG("Could not allocate video codec context\n")
        return false;
    }

    encoder->packet = av_packet_alloc();

    return true;
}

void deinitFrameEncoder(FrameEncoder *encoder) {
    NULLSAFE_CALL(&encoder->codecCtx, avcodec_free_context)
    NULLSAFE_CALL(&encoder->packet, av_packet_free)
}

bool createJPEGEncoder(FrameEncoder *encoder, int width, int height, int quality) {
    if (!initFrameEncoder(encoder, AV_CODEC_ID_MJPEG)) {
        goto failed;
    }

    encoder->codecCtx->bit_rate = 40000;
    encoder->codecCtx->width = width;
    encoder->codecCtx->height = height;
    encoder->codecCtx->pix_fmt = AV_PIX_FMT_YUVJ420P;
    encoder->codecCtx->codec_id = AV_CODEC_ID_MJPEG;
    encoder->codecCtx->codec_type = AVMEDIA_TYPE_VIDEO;
    encoder->codecCtx->time_base.num = 1;
    encoder->codecCtx->time_base.den = 25;
    encoder->codecCtx->qmin = 10;
    encoder->codecCtx->qmax = 51;
    encoder->codecCtx->qcompress = 0.5;
    encoder->codecCtx->max_b_frames = 0;
    encoder->codecCtx->max_qdiff = 10;
    encoder->codecCtx->flags |= AV_CODEC_FLAG_GLOBAL_HEADER;

    if (!openEncoder(encoder)) {
        goto failed;
    }

    return true;

    failed:
    deinitFrameEncoder(encoder);
    return false;
}

bool openEncoder(FrameEncoder *encoder) {
    if (avcodec_open2(encoder->codecCtx, encoder->codec, NULL) < 0) {
        LOG("Could not open codec\n")
        return false;
    }

    return true;
}

bool encodeFrame(FrameEncoder *encoder, AVFrame *frame) {
    if (avcodec_send_frame(encoder->codecCtx, frame) < 0) {
        LOG("Error sending frame to encoder\n")
        return false;
    }

    if (avcodec_receive_packet(encoder->codecCtx, encoder->packet) < 0) {
        LOG("Error receiving packet from encoder\n")
        return false;
    }

    return true;
}

bool writeEncoderPacketToFile(FrameEncoder *encoder, const char *filename) {
    // Write the encoded frame to file
    FILE *f = fopen(filename, "wb");
    if (!f) {
        LOG("Could not open %s\n", filename)
        return false;
    }

    fwrite(encoder->packet->data, 1, encoder->packet->size, f);
    fclose(f);

    return true;
}
