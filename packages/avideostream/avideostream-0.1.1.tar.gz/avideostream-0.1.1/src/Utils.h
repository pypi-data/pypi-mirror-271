#pragma once

#include <stdio.h>

#define DEBUG

#ifdef DEBUG
#define LOG(...) fprintf(stderr, __VA_ARGS__);
#else
#define LOG(...)
#endif

#define NULLSAFE_CALL(x, free) if (x != NULL) { free(x); }
