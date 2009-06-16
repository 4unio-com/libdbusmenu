import os
import gtk, gobject, wnck

def minimize_all_windows():
    def start_minimizing():
        for w in screen.get_windows():
            w.minimize()


    screen = wnck.screen_get_default()
    gobject.idle_add(start_minimizing)
    gobject.idle_add(gtk.main_quit)
    gtk.main()

def get_system_language():
    raise NotImplementedError, "not yet..."
