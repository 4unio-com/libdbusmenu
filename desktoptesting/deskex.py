from desktoptesting.gnome import Application
from time import time, sleep
import tempfile
import pynotify
import ldtp, ldtputils
import os
import gtk, glib

try:
    import indicate
except ImportError:
    indicate = None

class IndicatorApplet(Application):
    IA_TOPLEVEL = "embindicator-applet"
    def __init__(self):
        Application.__init__(self, 'indicator-applet')
        self.indicators = []
        self.server = None

    def open(self):
        pass
    
    def add_server(self, desktop_file):
        if not self.server:
            self.server = indicate.indicate_server_ref_default()
        self.server.set_type("message.im")
        self.server.set_desktop_file(desktop_file)
        self.server.show()
        while gtk.events_pending():
            gtk.main_iteration()

    def show_indicator(self, sender):
        indicator = indicate.IndicatorMessage()
        indicator.set_property("subtype", "im")
        indicator.set_property("sender", sender)
        indicator.set_property_time("time", time())
        pixbuf = gtk.gdk.pixbuf_new_from_file(
            "/usr/share/icons/hicolor/22x22/apps/gnome-freecell.png")
        indicator.set_property_icon("icon", pixbuf)
        indicator.show()
        self.indicators.append(indicator)
        while gtk.events_pending():
            gtk.main_iteration()

    def capture_applet_icon(self):
        x, y, w, h = ldtp.getobjectsize(self.TOP_PANEL, self.IA_TOPLEVEL)
        screeny = ldtputils.imagecapture(
            outFile=tempfile.mktemp('.png', 'ia_'),
            x=x, y=y, resolution1=w, resolution2=h)        
        return screeny

    def select_indicator(self, sender):
        ldtp.selectmenuitem(self.TOP_PANEL, 'mnu' + sender.replace(' ',''))

    def wait_for_indicator_display(self, sender, timeout=5):
        handlers = []
        displayed = [False]

        def _display_cb(indicator):
            indicator.hide() # This is just normal behavior, so why not?
            displayed[0] = True
            gtk.main_quit()
            
        def _timeout_cb():
            gtk.main_quit()
            return False

        for indicator in self.indicators:
            if sender == indicator.get_property("sender"):
                handler = indicator.connect("user-display", _display_cb)
                handlers.append((handler, indicator))

        glib.timeout_add_seconds(timeout, _timeout_cb)

        gtk.main()

        for handler, indicator in handlers:
            indicator.disconnect(handler)

        return displayed[0]

    def wait_for_server_display(self, timeout=5):
        displayed = [False]
        handler = 0

        def _display_cb(indicator):
            indicator.hide() # This is just normal behavior, so why not?
            displayed[0] = True
            gtk.main_quit()
            
        def _timeout_cb():
            gtk.main_quit()
            return False

        handler = self.server.connect("server-display", _display_cb)

        glib.timeout_add_seconds(timeout, _timeout_cb)

        gtk.main()

        self.server.disconnect(handler)

        return displayed[0]

    def cleanup(self):
        for indicator in self.indicators:
            indicator.hide()
        # BUG: 351537
        # self.server.hide()
        sleep(1)

    def close(self):
        self.cleanup()

    def setup(self):
        self.open()

    def teardown(self):
        self.close()

class NotifyOSD(Application):
    def __init__(self):
        self.focus_desktop = False
        self.screenshots = []

        if not pynotify.init('notify-osd-test'):
            raise ldtp.LdtpExecutionError, \
                "Failed to initialize notification connection."

        info = pynotify.get_server_info()
        if info.get('name', None) != 'notify-osd':
            raise ldtp.LdtpExecutionError, \
                "The notify service is '%s', expected 'notify-dameon'" % \
                info.get('name', None)

    def open(self, focus_desktop=True):
        self.focus_desktop = focus_desktop

        if self.focus_desktop:
            ldtp.generatekeyevent('<alt><ctrl>d')

    def exit(self):
        if self.focus_desktop:
            ldtp.generatekeyevent('<alt><ctrl>d')
        for screenshot in self.screenshots:
            os.remove(screenshot)

    def notify(self, summary, body="", icon=None):
	n = pynotify.Notification (summary, body, icon)
	n.show ()

    def notify_synchronous(self, summary, body="", icon=None, value=-1):
	n = pynotify.Notification (summary, body, icon)
        n.set_hint("synchronous", "volume")
        n.set_hint("value", value)
	n.show ()

    def grab_image_and_wait(self, summary):
        ldtp.waittillguiexist(summary)
        start_time = time()
        x, y, w, h = ldtp.getwindowsize(summary)
        screenshot = \
            ldtputils.imagecapture(outFile=tempfile.mktemp('.png', 'nosd_'),
                                   x=x+3, y=y+3, 
                                   resolution1=w-6, 
                                   resolution2=h-6)
        ldtp.waittillguinotexist(summary)
        end_time = time() - start_time
        self.screenshots.append(screenshot)
        return (end_time, screenshot)

    def get_extents(self, summary, wait=False):
        if wait:
            exists = ldtp.waittillguiexist(summary)            
        else:
            exists = ldtp.guiexist(summary)            
            
        if exists:
            return ldtp.getwindowsize(summary)
        else:
            return -1, -1, -1, -1
            
if __name__ == "__main__":
    from time import sleep
    test = IndicatorApplet()
    test.open()
    test.add_server('/usr/share/applications/pidgin.desktop')
    test.show_indicator('Elmer Fud')
    print test.wait_for_indicator_display('Elmer Fud', 20)
