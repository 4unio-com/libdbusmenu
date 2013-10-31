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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "gmenu-translator.h"

struct _DbusmenuGmenuTranslatorPrivate {
	int dummy;
};

#define DBUSMENU_GMENU_TRANSLATOR_GET_PRIVATE(o) \
(G_TYPE_INSTANCE_GET_PRIVATE ((o), DBUSMENU_TYPE_GMENU_TRANSLATOR, DbusmenuGmenuTranslatorPrivate))

static void dbusmenu_gmenu_translator_class_init (DbusmenuGmenuTranslatorClass *klass);
static void dbusmenu_gmenu_translator_init       (DbusmenuGmenuTranslator *self);
static void dbusmenu_gmenu_translator_dispose    (GObject *object);
static void dbusmenu_gmenu_translator_finalize   (GObject *object);
static void ag_init                              (GObject *object);

G_DEFINE_TYPE_WITH_CODE (DbusmenuGmenuTranslator, dbusmenu_gmenu_translator, G_TYPE_MENU_MODEL,
                         G_IMPLEMENT_INTERFACE(G_TYPE_ACTION_GROUP, ag_init));

static void
dbusmenu_gmenu_translator_class_init (DbusmenuGmenuTranslatorClass *klass)
{
	GObjectClass *object_class = G_OBJECT_CLASS (klass);

	g_type_class_add_private (klass, sizeof (DbusmenuGmenuTranslatorPrivate));

	object_class->dispose = dbusmenu_gmenu_translator_dispose;
	object_class->finalize = dbusmenu_gmenu_translator_finalize;
}

static void
dbusmenu_gmenu_translator_init (DbusmenuGmenuTranslator *self)
{
}

static void
ag_init (GObject * object)
{
}

static void
dbusmenu_gmenu_translator_dispose (GObject *object)
{

	G_OBJECT_CLASS (dbusmenu_gmenu_translator_parent_class)->dispose (object);
}

static void
dbusmenu_gmenu_translator_finalize (GObject *object)
{

	G_OBJECT_CLASS (dbusmenu_gmenu_translator_parent_class)->finalize (object);
}
