#include "VideoStream.h"

void initVideoStream(VideoStream *stream, const char *uri) {
    avformat_network_init();

    stream->uri = uri;
    stream->fmtCtx = avformat_alloc_context();

    memset(&stream->packet, 0, sizeof(stream->packet));
    memset(&stream->image, 0, sizeof(stream->image));

    stream->frame = NULL;

    stream->frameNumber = 0;
    stream->videoStreamIndex = -1;
    stream->codecParams = NULL;
    stream->codecCtx = NULL;
}

void deinitVideoStream(VideoStream *stream) {
    NULLSAFE_CALL(stream->codecCtx, avcodec_close)
    NULLSAFE_CALL(&stream->fmtCtx, avformat_close_input)
    NULLSAFE_CALL(stream->fmtCtx, avformat_free_context)
    NULLSAFE_CALL(&stream->frame, av_frame_free)
    NULLSAFE_CALL(&stream->packet, av_packet_unref)

    avformat_network_deinit();
}

void dumpVideoStreamInfo(VideoStream *stream) {
    av_dump_format(stream->fmtCtx, 0, stream->uri, 0);
}

bool openVideoStream(VideoStream *stream) {
    if (avformat_open_input(&stream->fmtCtx, stream->uri, NULL, NULL) != 0) {
        LOG("Could not open stream to %s\n", stream->uri)
        return false;
    }

    if (avformat_find_stream_info(stream->fmtCtx, NULL) < 0) {
        LOG("Could not find stream info\n")
        return false;
    }

    for (int i = 0; i < stream->fmtCtx->nb_streams; i++) {
        AVCodecParameters *par = stream->fmtCtx->streams[i]->codecpar;

        if (AVMEDIA_TYPE_VIDEO == par->codec_type && stream->videoStreamIndex < 0) {
            stream->videoStreamIndex = i;
            stream->codecParams = par;
            break;
        }
    }

    if (stream->videoStreamIndex < 0) {
        LOG("No video stream found\n")
        return false;
    }

    stream->image.height = stream->codecParams->height;
    stream->image.width = stream->codecParams->width;

    const AVCodec *codec = avcodec_find_decoder(stream->codecParams->codec_id);

    if (codec == NULL) {
        LOG("Unsupported codec\n")
        return false;
    }

    stream->codecCtx = avcodec_alloc_context3(codec);

    if (avcodec_parameters_to_context(stream->codecCtx, stream->codecParams) < 0) {
        LOG("Could not copy codec parameters to decoder context\n")
        return false;
    }

    if (avcodec_open2(stream->codecCtx, codec, NULL) < 0) {
        LOG("Could not open codec\n")
        return false;
    }

    stream->frame = av_frame_alloc();
    stream->frame->format = stream->codecCtx->pix_fmt;
    stream->frame->width = stream->codecCtx->width;
    stream->frame->height = stream->codecCtx->height;

    return true;
}

bool createVideoStream(VideoStream *stream, const char *uri) {
    initVideoStream(stream, uri);

    if (!openVideoStream(stream)) {
        deinitVideoStream(stream);
        return false;
    }

    return true;
}

bool readFrame(VideoStream *stream) {
    static const size_t max_read_attempts = 4096;
    static const size_t max_decode_attempts = 64;

    size_t cur_read_attempts = 0;
    size_t cur_decode_attempts = 0;

    bool valid = false;

    // Ensure consumed frames are not exceeding the total number of frames
    // that the video stream has provided
    if (stream->fmtCtx->streams[stream->videoStreamIndex]->nb_frames > 0 &&
        stream->frameNumber > stream->fmtCtx->streams[stream->videoStreamIndex]->nb_frames) {
        LOG("No more frames to read\n")
        return false;
    }

    // check if we can receive frame from previously decoded packet
    valid = avcodec_receive_frame(stream->codecCtx, stream->frame) >= 0;

    // get the next frame
    while (!valid) {
        int ret = av_read_frame(stream->fmtCtx, &stream->packet);

        if (ret == AVERROR(EAGAIN))
            continue;

        if (ret == AVERROR_EOF) {
            // flush cached frames from video decoder
            stream->packet.data = NULL;
            stream->packet.size = 0;
            stream->packet.stream_index = stream->videoStreamIndex;
        }

        if (stream->packet.stream_index != stream->videoStreamIndex) {
            NULLSAFE_CALL(&stream->packet, av_packet_unref)

            if (++cur_read_attempts > max_read_attempts) {
                LOG("Error reading frame after %zu attempts\n", max_read_attempts)
                break;
            }

            continue;
        }

        // Decode video frame
        if (avcodec_send_packet(stream->codecCtx, &stream->packet) < 0) {
            LOG("Error sending packet to decoder\n")
            break;
        }

        ret = avcodec_receive_frame(stream->codecCtx, stream->frame);

        if (ret >= 0) {
            valid = true;
        } else if (ret == AVERROR(EAGAIN)) {
            continue;
        } else {
            if (++cur_decode_attempts > max_decode_attempts) {
                LOG("Error decoding frame after %zu attempts\n", max_decode_attempts)
                break;
            }
        }
    }


    if (valid) {
        stream->frameNumber++;
    }

    return valid;
}


