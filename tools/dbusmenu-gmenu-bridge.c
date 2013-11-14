
#include <gio/gio.h>

const gchar * dbus_name = NULL;
const gchar * object_path = NULL;
const gchar * dbusmenu_name = NULL;
const gchar * dbusmenu_path = NULL;
GMainLoop * mainloop = NULL;


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

	mainloop = g_main_loop_new(NULL, FALSE);
	g_main_loop_run(mainloop);
	g_main_loop_unref(mainloop);

	return 0;
}
