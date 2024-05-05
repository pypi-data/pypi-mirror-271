//
// Created by javad on 24-03-24.
//
#include "VideoStream.h"
#include "FrameEncoding.h"

int main(int argc, char **argv) {
    if (argc < 2) {
        printf("Usage: %s <url>\n", argv[0]);
        return 1;
    }

    const char *url = argv[1];

    VideoStream stream;
    FrameEncoder encoder;

    if (!createVideoStream(&stream, url)) {
        printf("Failed to create video stream\n");
        return 1;
    }

    dumpVideoStreamInfo(&stream);

    if (!createJPEGEncoder(&encoder, stream.image.width, stream.image.height, 100)) {
        printf("Failed to create JPEG encoder\n");
        return 1;
    }

    while (stream.frameNumber < 10) {
        // read frame
        if (!readFrame(&stream)) {
            break;
        }

        encodeFrame(&encoder, stream.frame);

        // Print width and height of the frame
        printf("Width: %d, Height: %d\n", stream.image.width, stream.image.height);

        // Write the image to a file
        char *filename = malloc(100);
        sprintf(filename, "frame_%lu.jpg", stream.frameNumber);
        writeEncoderPacketToFile(&encoder, filename);
    }

    deinitVideoStream(&stream);
    deinitFrameEncoder(&encoder);
}