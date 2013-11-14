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
#include "menuitem.h"

#define ACTION_PREFIX "dbusmenu-translator-"

struct _DbusmenuGmenuTranslatorPrivate {
	GHashTable * item_lookup;
	DbusmenuMenuitem * root;
};

/* Properties */
enum {
	PROP_0,
	PROP_ROOT,
	PROP_COUNT
};

#define DBUSMENU_GMENU_TRANSLATOR_GET_PRIVATE(o) \
(G_TYPE_INSTANCE_GET_PRIVATE ((o), DBUSMENU_TYPE_GMENU_TRANSLATOR, DbusmenuGmenuTranslatorPrivate))

static void dbusmenu_gmenu_translator_class_init (DbusmenuGmenuTranslatorClass *klass);
static void dbusmenu_gmenu_translator_init       (DbusmenuGmenuTranslator *self);
static void dbusmenu_gmenu_translator_dispose    (GObject *object);
static void dbusmenu_gmenu_translator_finalize   (GObject *object);
static void constructed                          (GObject * obj);
static void ag_init                              (GObject *object);
static void set_property (GObject * obj, guint id, const GValue * value, GParamSpec * pspec);
static void get_property (GObject * obj, guint id, GValue * value, GParamSpec * pspec);
static void add_menuitem (DbusmenuGmenuTranslator * self, DbusmenuMenuitem * item);

G_DEFINE_TYPE_WITH_CODE (DbusmenuGmenuTranslator, dbusmenu_gmenu_translator, G_TYPE_MENU_MODEL,
                         G_IMPLEMENT_INTERFACE(G_TYPE_ACTION_GROUP, ag_init));

static void
dbusmenu_gmenu_translator_class_init (DbusmenuGmenuTranslatorClass *klass)
{
	GObjectClass *object_class = G_OBJECT_CLASS (klass);

	g_type_class_add_private (klass, sizeof (DbusmenuGmenuTranslatorPrivate));

	object_class->dispose = dbusmenu_gmenu_translator_dispose;
	object_class->finalize = dbusmenu_gmenu_translator_finalize;
	object_class->set_property = set_property;
	object_class->get_property = get_property;
	object_class->constructed = constructed;

	g_object_class_install_property(object_class, PROP_ROOT,
	                                g_param_spec_object("root", "Root DBusmenu Menuitem",
	                                                    "The root of the menu structure being translated",
	                                                    DBUSMENU_TYPE_MENUITEM,
	                                                    G_PARAM_CONSTRUCT_ONLY | G_PARAM_READWRITE | G_PARAM_STATIC_STRINGS));
}

static void
dbusmenu_gmenu_translator_init (DbusmenuGmenuTranslator *self)
{
	self->priv = DBUSMENU_GMENU_TRANSLATOR_GET_PRIVATE(self);

	self->priv->item_lookup = g_hash_table_new_full(g_int_hash, g_int_equal, NULL, g_object_unref);
}

static void
ag_init (GObject * object)
{
}

static void
constructed (GObject * obj)
{
	DbusmenuGmenuTranslator * self = DBUSMENU_GMENU_TRANSLATOR(obj);

	if (self->priv->root == NULL) {
		g_critical("No Root item!");
		return;
	}

	add_menuitem(self, self->priv->root);
}

static void
set_property (GObject * obj, guint id, const GValue * value, GParamSpec * pspec)
{
	DbusmenuGmenuTranslator * self = DBUSMENU_GMENU_TRANSLATOR(obj);

	switch (id) {
	case PROP_ROOT:
		g_clear_object(&self->priv->root);
		self->priv->root = g_value_dup_object(value);
		break;
	default:
		G_OBJECT_WARN_INVALID_PROPERTY_ID(obj, id, pspec);
		break;
	}
}

static void
get_property (GObject * obj, guint id, GValue * value, GParamSpec * pspec)
{
	DbusmenuGmenuTranslator * self = DBUSMENU_GMENU_TRANSLATOR(obj);

	switch (id) {
	case PROP_ROOT:
		g_value_set_object(value, self->priv->root);
		break;
	default:
		G_OBJECT_WARN_INVALID_PROPERTY_ID(obj, id, pspec);
		break;
	}
}

static void
dbusmenu_gmenu_translator_dispose (GObject *object)
{
	DbusmenuGmenuTranslator * self = DBUSMENU_GMENU_TRANSLATOR(object);

	g_hash_table_remove_all(self->priv->item_lookup);
	g_clear_object(&self->priv->root);

	G_OBJECT_CLASS (dbusmenu_gmenu_translator_parent_class)->dispose (object);
}

static void
dbusmenu_gmenu_translator_finalize (GObject *object)
{
	DbusmenuGmenuTranslator * self = DBUSMENU_GMENU_TRANSLATOR(object);

	g_hash_table_destroy(self->priv->item_lookup);

	G_OBJECT_CLASS (dbusmenu_gmenu_translator_parent_class)->finalize (object);
}

/* Adds a menu item, signaling it's menus being created as well as actions */
static void
add_menuitem (DbusmenuGmenuTranslator * self, DbusmenuMenuitem * item)
{
	gint item_id = dbusmenu_menuitem_get_id(item);

	/* Look at the hash table, but not for the root item */
	if (item_id != 0) {
		if (g_hash_table_contains(self->priv->item_lookup, GINT_TO_POINTER(item_id))) {
			/* we already have this one */
			return;
		}

		/* Okay, we're keeping this one */
		g_hash_table_insert(self->priv->item_lookup, GINT_TO_POINTER(item_id), g_object_ref(item));
	}

	/* Recurse through the children first */
	GList * child;
	for (child = dbusmenu_menuitem_get_children(item); child != NULL; child = g_list_next(child)) {
		add_menuitem(self, DBUSMENU_MENUITEM(child->data));
	}

	/* For root we don't need to do anything else */
	if (dbusmenu_menuitem_get_root(item)) {
		return;
	}

	gchar * action_name = g_strdup_printf(ACTION_PREFIX "%d", item_id);
	g_signal_emit_by_name(self, "action-added", action_name);
	g_free(action_name);
}
