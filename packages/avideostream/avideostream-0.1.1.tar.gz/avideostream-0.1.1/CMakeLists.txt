cmake_minimum_required(VERSION 3.27)
project(avideostream)

# Find the required ffmpeg libraries
find_package(PkgConfig REQUIRED)
pkg_check_modules(AVFORMAT REQUIRED libavformat)
pkg_check_modules(AVCODEC REQUIRED libavcodec)
pkg_check_modules(AVUTIL REQUIRED libavutil)

# Find python
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

# Include ffmpeg headers
include_directories(${AVFORMAT_INCLUDE_DIRS} ${AVCODEC_INCLUDE_DIRS} ${AVUTIL_INCLUDE_DIRS} ${Python3_INCLUDE_DIRS})
include_directories(src)

add_library(VideoStream SHARED
        src/VideoStream.c
        src/FrameEncoding.c
)

target_link_libraries(VideoStream ${AVFORMAT_LIBRARIES} ${AVCODEC_LIBRARIES} ${AVUTIL_LIBRARIES})

add_library(VideoStreamPy MODULE
        src/avideostream.c
)

target_link_libraries(VideoStreamPy VideoStream ${Python3_LIBRARIES})

add_executable(main src/main.c)

target_link_libraries(main VideoStream)


