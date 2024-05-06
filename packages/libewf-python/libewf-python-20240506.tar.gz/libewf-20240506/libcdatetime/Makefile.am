if HAVE_LOCAL_LIBCDATETIME
AM_CPPFLAGS = \
	-I../include -I$(top_srcdir)/include \
	-I../common -I$(top_srcdir)/common \
	@LIBCERROR_CPPFLAGS@ 

noinst_LTLIBRARIES = libcdatetime.la

libcdatetime_la_SOURCES = \
	libcdatetime_definitions.h \
	libcdatetime_elements.c libcdatetime_elements.h \
	libcdatetime_error.c libcdatetime_error.h \
	libcdatetime_extern.h \
	libcdatetime_libcerror.h \
	libcdatetime_timestamp.c libcdatetime_timestamp.h \
	libcdatetime_support.c libcdatetime_support.h \
	libcdatetime_types.h \
	libcdatetime_unused.h
endif

DISTCLEANFILES = \
	Makefile \
	Makefile.in

sources-local: $(BUILT_SOURCES)

splint-local:
	@echo "Running splint on libcdatetime ..."
	-splint -preproc -redef $(DEFS) $(DEFAULT_INCLUDES) $(INCLUDES) $(AM_CPPFLAGS) $(libcdatetime_la_SOURCES)

