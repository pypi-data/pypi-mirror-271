from setuptools import setup, Extension, find_packages

setup(
    name="avideostream",
    version="0.1.1",
    author="SimplyPrint",
    author_email="javad.asgari@simplyprint.io",
    description="Directly use libav (ffmpeg) to read RTSP streams with python bindings.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    ext_modules=[
        Extension(
            "avideostream",
            sources=[
                "src/avideostream.c",
                "src/VideoStream.c",
                "src/FrameEncoding.c"
            ],
            libraries=['avformat', 'avcodec', 'avutil'],
        )
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
