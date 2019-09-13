# Makefile for HDTV::Display
MODNAME = display

include ../Makefile.def

CFLAGS   += $(LIBX11_CFLAGS)
CXXFLAGS += $(LIBX11_CFLAGS) -I../calibration

LDFLAGS  += $(LIBX11_LDFLAGS)

LDLIBS   += $(ROOT_GLIBS) -lX11

ROOT_CLING_FLAGS += $(LIBX11_CFLAGS) -I../calibration

include ../Makefile.body
