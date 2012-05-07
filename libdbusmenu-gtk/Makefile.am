
GTKGIR=Gtk-3.0
GTKVALA=gtk+-3.0
lib_LTLIBRARIES = libdbusmenu-gtk3.la

BUILT_SOURCES = 
CLEANFILES = 
DISTCLEANFILES = 
EXTRA_DIST = \
	dbusmenu-gtk-0.4.pc.in \
	dbusmenu-gtk3-0.4.pc.in

##############
# Enum Stuff
##############

include $(top_srcdir)/Makefile.am.enum

glib_enum_h = genericmenuitem-enum-types.h
glib_enum_c = genericmenuitem-enum-types.c
glib_enum_headers = $(srcdir)/genericmenuitem.h


#####################
# Include Directory
#####################

libdbusmenu_gtkincludedir=$(includedir)/libdbusmenu-gtk3-0.4/libdbusmenu-gtk/

libdbusmenu_gtkinclude_HEADERS = \
	dbusmenu-gtk.h \
	client.h \
	menu.h \
	menuitem.h \
	parser.h

libdbusmenu_gtk_la_SOURCES = \
	client.h \
	client.c \
	genericmenuitem.h \
	genericmenuitem.c \
	genericmenuitem-enum-types.h \
	genericmenuitem-enum-types.c \
	menu.h \
	menu.c \
	menuitem.h \
	menuitem.c \
	parser.h \
	parser.c

libdbusmenu_gtk_la_LDFLAGS = \
	$(COVERAGE_LDFLAGS) \
	-version-info $(LIBDBUSMENU_CURRENT):$(LIBDBUSMENU_REVISION):$(LIBDBUSMENU_AGE) \
	-no-undefined \
	-export-symbols-regex "^[^_].*"

libdbusmenu_gtk_la_CFLAGS = \
	$(DBUSMENUGTK_CFLAGS) \
	$(COVERAGE_CFLAGS) \
	-I$(top_srcdir) \
	-Wall -Werror -Wno-error=deprecated-declarations \
	-DG_LOG_DOMAIN="\"LIBDBUSMENU-GTK\""

libdbusmenu_gtk_la_LIBADD = \
	$(top_builddir)/libdbusmenu-glib/libdbusmenu-glib.la \
	$(DBUSMENUGTK_LIBS)

libdbusmenu_gtk3includedir = $(libdbusmenu_gtkincludedir)
libdbusmenu_gtk3include_HEADERS = $(libdbusmenu_gtkinclude_HEADERS)
libdbusmenu_gtk3_la_SOURCES = $(libdbusmenu_gtk_la_SOURCES)
libdbusmenu_gtk3_la_LDFLAGS = $(libdbusmenu_gtk_la_LDFLAGS)
libdbusmenu_gtk3_la_CFLAGS = $(libdbusmenu_gtk_la_CFLAGS)
libdbusmenu_gtk3_la_LIBADD = $(libdbusmenu_gtk_la_LIBADD)

pkgconfig_DATA = dbusmenu-gtk3-0.4.pc
pkgconfigdir = $(libdir)/pkgconfig

#########################
# GObject Introsepction 
#########################

-include $(INTROSPECTION_MAKEFILE)
INTROSPECTION_GIRS = 

if INTROSPECTION_TEN
INTROSPECTION_SCANNER_ARGS = --add-include-path=$(srcdir) \
	--warn-all \
	--add-include-path=$(top_builddir)/libdbusmenu-glib \
	$(addprefix --c-include=libdbusmenu-gtk/, $(libdbusmenu_gtkinclude_HEADERS)) \
	--symbol-prefix=dbusmenu \
	--identifier-prefix=DbusmenuGtk
else
INTROSPECTION_SCANNER_ARGS = --add-include-path=$(srcdir) \
	--warn-all \
	--add-include-path=$(top_builddir)/libdbusmenu-glib \
	$(addprefix --c-include=libdbusmenu-gtk/, $(libdbusmenu_gtkinclude_HEADERS))
endif

INTROSPECTION_COMPILER_ARGS = --includedir=$(builddir) --includedir=$(top_builddir)/libdbusmenu-glib

if HAVE_INTROSPECTION

introspection_sources = $(filter-out genericmenuitem%, $(libdbusmenu_gtkinclude_HEADERS) $(libdbusmenu_gtk_la_SOURCES))

DbusmenuGtk3-0.4.gir: libdbusmenu-gtk3.la
DbusmenuGtk3_0_4_gir_INCLUDES = \
	GObject-2.0 \
	$(GTKGIR) \
	Dbusmenu-0.4 
DbusmenuGtk3_0_4_gir_CFLAGS = \
	$(DBUSMENUGTK_CFLAGS) \
	-I$(top_srcdir)
DbusmenuGtk3_0_4_gir_LIBS = libdbusmenu-gtk3.la \
	$(top_builddir)/libdbusmenu-glib/libdbusmenu-glib.la
DbusmenuGtk3_0_4_gir_FILES = $(addprefix $(srcdir)/, $(introspection_sources))
DbusmenuGtk3_0_4_gir_NAMESPACE = DbusmenuGtk3
DbusmenuGtk3_0_4_gir_EXPORT_PACKAGES = dbusmenu-gtk3-0.4

INTROSPECTION_GIRS += DbusmenuGtk3-0.4.gir

girdir = $(datadir)/gir-1.0
gir_DATA = $(INTROSPECTION_GIRS)

typelibdir = $(libdir)/girepository-1.0
typelib_DATA = $(INTROSPECTION_GIRS:.gir=.typelib)

CLEANFILES += $(gir_DATA) $(typelib_DATA)

endif

#########################
# VAPI Files
#########################

if HAVE_VALA
if HAVE_INTROSPECTION

vapidir = $(datadir)/vala/vapi
vapi_DATA = dbusmenu-gtk3-0.4.vapi

dbusmenu-gtk3-0.4.vapi: DbusmenuGtk3-0.4.tmp.gir Makefile.am
	$(VALA_API_GEN) --library=dbusmenu-gtk3-0.4 \
		--pkg gdk-pixbuf-2.0 \
		--pkg $(GTKVALA) \
		--pkg atk \
		--pkg dbusmenu-glib-0.4 \
		--vapidir=$(top_builddir)/libdbusmenu-glib \
		$<

DbusmenuGtk3-0.4.tmp.gir: DbusmenuGtk3-0.4.gir
	$(SED) \
		-e "s|GdkPixbuf.Pixbuf|Gdk.Pixbuf|g" \
		-e "s|Atk.ImplementorIface|Atk.Implementor|g" \
		$< > $@

CLEANFILES += $(vapi_DATA) DbusmenuGtk3-0.4.tmp.gir

endif
endif

