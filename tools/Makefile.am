
SUBDIRS = testapp

libexec_PROGRAMS =

if WANT_DBUSMENUDUMPER
libexec_PROGRAMS += dbusmenu-dumper
endif

libexec_SCRIPTS = dbusmenu-bench

dbusmenu_dumper_SOURCES = \
	dbusmenu-dumper.c

dbusmenu_dumper_CFLAGS = \
	-I $(srcdir)/.. \
	$(DBUSMENUGLIB_CFLAGS) \
	$(DBUSMENUDUMPER_CFLAGS) \
	-Wall -Werror

dbusmenu_dumper_LDADD = \
	../libdbusmenu-glib/libdbusmenu-glib.la \
	$(DBUSMENUGLIB_LIBS) \
	$(DBUSMENUDUMPER_LIBS)

doc_DATA = README.dbusmenu-bench

noinst_PROGRAMS = \
	dbusmenu-gmenu-bridge

dbusmenu_gmenu_bridge_SOURCES = \
	dbusmenu-gmenu-bridge.c

dbusmenu_gmenu_bridge_CFLAGS = \
	-I $(srcdir)/.. \
	$(DBUSMENUGLIB_CFLAGS) \
	-Wall -Werror

dbusmenu_gmenu_bridge_LDADD = \
	../libdbusmenu-glib/libdbusmenu-glib.la \
	$(DBUSMENUGLIB_LIBS)

EXTRA_DIST = \
	$(doc_DATA) \
	dbusmenu-bench
