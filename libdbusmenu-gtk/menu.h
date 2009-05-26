#ifndef __DBUSMENU_GTKMENU_H__
#define __DBUSMENU_GTKMENU_H__

#include <glib.h>
#include <glib-object.h>

G_BEGIN_DECLS

#define DBUSMENU_GTKMENU_TYPE            (dbusmenu_gtkmenu_get_type ())
#define DBUSMENU_GTKMENU(obj)            (G_TYPE_CHECK_INSTANCE_CAST ((obj), DBUSMENU_GTKMENU_TYPE, DbusmenuGtkMenu))
#define DBUSMENU_GTKMENU_CLASS(klass)    (G_TYPE_CHECK_CLASS_CAST ((klass), DBUSMENU_GTKMENU_TYPE, DbusmenuGtkMenuClass))
#define DBUSMENU_IS_GTKMENU(obj)         (G_TYPE_CHECK_INSTANCE_TYPE ((obj), DBUSMENU_GTKMENU_TYPE))
#define DBUSMENU_IS_GTKMENU_CLASS(klass) (G_TYPE_CHECK_CLASS_TYPE ((klass), DBUSMENU_GTKMENU_TYPE))
#define DBUSMENU_GTKMENU_GET_CLASS(obj)  (G_TYPE_INSTANCE_GET_CLASS ((obj), DBUSMENU_GTKMENU_TYPE, DbusmenuGtkMenuClass))

/**
	DbusmenuGtkMenuClass:
	@parent_class: #GtkMenuClass
	@reserved1: Reserved for future use.
	@reserved2: Reserved for future use.
	@reserved3: Reserved for future use.
	@reserved4: Reserved for future use.
*/
typedef struct _DbusmenuGtkMenuClass DbusmenuGtkMenuClass;
struct _DbusmenuGtkMenuClass {
	GtkMenuClass parent_class;

	/* Reserved */
	void (*reserved1) (void);
	void (*reserved2) (void);
	void (*reserved3) (void);
	void (*reserved4) (void);
};

/**
	DbusmenuGtkMenu:
	@parent: #GtkMenu
*/
typedef struct _DbusmenuGtkMenu      DbusmenuGtkMenu;
struct _DbusmenuGtkMenu {
	GtkMenu parent;
};

GType dbusmenu_gtkmenu_get_type (void);
DbusmenuGtkMenu * dbusmenu_gtkmenu_new (gchar * dbus_name, gchar * dbus_object);

/**
	SECTION:gtkmenu
	@short_description: A GTK Menu Object that syncronizes over DBus
	@stability: Unstable
	@include: libdbusmenu-gtk/menu.h

	In general, this is just a #GtkMenu, why else would you care?  Oh,
	because this menu is created by someone else on a server that exists
	on the other side of DBus.  You need a #DbusmenuServer to be able
	push the data into this menu.

	The first thing you need to know is how to find that #DbusmenuServer
	on DBus.  This involves both the DBus name and the DBus object that
	the menu interface can be found on.  Those two value should be set
	when creating the object using dbusmenu_gtkmenu_new().  They are then
	stored on two properties #DbusmenuGtkMenu:dbus-name and #DbusmenuGtkMenu:dbus-object.

	After creation the #DbusmenuGtkMenu it will continue to keep in
	synchronization with the #DbusmenuServer object across Dbus.  If the
	number of entries change, the menus change, if they change thier
	properties change, they update in the items.  All of this should
	be handled transparently to the user of this object.

	TODO: Document properties.
*/
G_END_DECLS

#endif