/*
A library to communicate a menu object set accross DBus and
track updates and maintain consistency.

Copyright 2013 Canonical Ltd.

Authors:
    Ted Gould <ted@canonical.com>

This program is free software: you can redistribute it and/or modify it 
under the terms of either or both of the following licenses:

1) the GNU Lesser General Public License version 3, as published by the 
Free Software Foundation; and/or
2) the GNU Lesser General Public License version 2.1, as published by 
the Free Software Foundation.

This program is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranties of 
MERCHANTABILITY, SATISFACTORY QUALITY or FITNESS FOR A PARTICULAR 
PURPOSE.  See the applicable version of the GNU Lesser General Public 
License for more details.

You should have received a copy of both the GNU Lesser General Public 
License version 3 and version 2.1 along with this program.  If not, see 
<http://www.gnu.org/licenses/>
*/

#ifndef __DBUSMENU_GMENU_TRANSLATOR_H__
#define __DBUSMENU_GMENU_TRANSLATOR_H__

#include <gio/gio.h>

G_BEGIN_DECLS

#define DBUSMENU_TYPE_GMENU_TRANSLATOR            (dbusmenu_gmenu_translator_get_type ())
#define DBUSMENU_GMENU_TRANSLATOR(obj)            (G_TYPE_CHECK_INSTANCE_CAST ((obj), DBUSMENU_TYPE_GMENU_TRANSLATOR, DbusmenuGmenuTranslator))
#define DBUSMENU_GMENU_TRANSLATOR_CLASS(klass)    (G_TYPE_CHECK_CLASS_CAST ((klass), DBUSMENU_TYPE_GMENU_TRANSLATOR, DbusmenuGmenuTranslatorClass))
#define DBUSMENU_IS_GMENU_TRANSLATOR(obj)         (G_TYPE_CHECK_INSTANCE_TYPE ((obj), DBUSMENU_TYPE_GMENU_TRANSLATOR))
#define DBUSMENU_IS_GMENU_TRANSLATOR_CLASS(klass) (G_TYPE_CHECK_CLASS_TYPE ((klass), DBUSMENU_TYPE_GMENU_TRANSLATOR))
#define DBUSMENU_GMENU_TRANSLATOR_GET_CLASS(obj)  (G_TYPE_INSTANCE_GET_CLASS ((obj), DBUSMENU_TYPE_GMENU_TRANSLATOR, DbusmenuGmenuTranslatorClass))

typedef struct _DbusmenuGmenuTranslator          DbusmenuGmenuTranslator;
typedef struct _DbusmenuGmenuTranslatorClass     DbusmenuGmenuTranslatorClass;
typedef struct _DbusmenuGmenuTranslatorPrivate   DbusmenuGmenuTranslatorPrivate;

struct _DbusmenuGmenuTranslatorClass {
	GMenuModelClass parent_class;
};

struct _DbusmenuGmenuTranslator {
	GMenuModel parent;
	DbusmenuGmenuTranslatorPrivate * priv;
};

GType dbusmenu_gmenu_translator_get_type (void);

G_END_DECLS

#endif
