
#include <gio/gio.h>
#include "libdbusmenu-glib/dbusmenu-glib.h"

const gchar * dbus_name = NULL;
const gchar * object_path = NULL;
const gchar * dbusmenu_name = NULL;
const gchar * dbusmenu_path = NULL;
GMainLoop * mainloop = NULL;
DbusmenuClient * client = NULL;
gboolean request_name = FALSE;

guint ag_export = 0;
guint menu_export = 0;
DbusmenuGmenuTranslator * bridge = NULL;


static void
root_changed (DbusmenuClient * client, DbusmenuMenuitem * root, gpointer user_data)
{
	GDBusConnection * bus = g_bus_get_sync(G_BUS_TYPE_SESSION, NULL, NULL);

	if (ag_export != 0) {
		g_dbus_connection_unexport_action_group(bus, ag_export);
		ag_export = 0;
	}

	if (menu_export != 0) {
		g_dbus_connection_unexport_menu_model(bus, menu_export);
		menu_export = 0;
	}

	g_clear_object(&bridge);
	bridge = dbusmenu_gmenu_translator_new(root);

	ag_export = g_dbus_connection_export_action_group(bus, object_path, G_ACTION_GROUP(bridge), NULL);
	menu_export = g_dbus_connection_export_menu_model(bus, object_path, G_MENU_MODEL(bridge), NULL);

	if (!request_name) {
		g_bus_own_name(G_BUS_TYPE_SESSION,
		               dbus_name,
		               G_BUS_NAME_OWNER_FLAGS_NONE,
		               NULL, /* bus acquired */
		               NULL, /* name acquired */
		               NULL, /* name lost */
		               NULL, /* user data */
		               NULL); /* user data free */
		request_name = TRUE;
	}

	g_object_unref(bus);
}

int
main (int argc, char * argv[])
{
	if (argc != 5) {
		g_printerr("Usage: %s [dbus name] [gmenu object path] [dbusmenu name] [dbusmenu object path]\n", argv[0]);
		return 1;
	}
	
	dbus_name = argv[1];
	object_path = argv[2];
	dbusmenu_name = argv[3];
	dbusmenu_path = argv[4];

	client = dbusmenu_client_new(dbusmenu_name, dbusmenu_path);
	g_signal_connect(G_OBJECT(client), DBUSMENU_CLIENT_SIGNAL_ROOT_CHANGED, G_CALLBACK(root_changed), NULL);


	mainloop = g_main_loop_new(NULL, FALSE);
	g_main_loop_run(mainloop);
	g_main_loop_unref(mainloop);

	g_object_unref(client);

	return 0;
}
