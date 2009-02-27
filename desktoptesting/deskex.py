from desktoptesting.gnome import Application
from time import time
import pynotify
import ldtp, ldtputils

class NotifyOSD(Application):
    def __init__(self):
        self.focus_desktop = False

    def open(self, focus_desktop=True):
        self.focus_desktop = focus_desktop

        if not pynotify.init('notify-osd-test'):
            raise ldtp.LdtpExecutionError, \
                "Failed to initialize notification connection."

        info = pynotify.get_server_info()
        if info.get('name', None) != 'notify-osd':
            raise ldtp.LdtpExecutionError, \
                "The notify service is '%s', expected 'notify-dameon'" % \
                info.get('name', None)

        if self.focus_desktop:
            ldtp.generatekeyevent('<alt><ctrl>d')

    def exit(self):
        if self.focus_desktop:
            ldtp.generatekeyevent('<alt><ctrl>d')

    def show_icon_summary_body(self, summary, body="", icon=None):
	n = pynotify.Notification (summary, body, icon)
	n.show ()
        ldtp.waittillguiexist(summary)
        start_time = time()
        x, y, w, h = ldtp.getwindowsize(summary)
        print x, y, w, h
        screenshot = \
            ldtputils.imagecapture(x=x, y=y, resolution1=w, resolution2=h)
        print 'Quick! Do something!'
        print ldtp.appundertest('notify-osd')
        ldtp.waittillguinotexist(summary)
        end_time = time() - start_time
        return (end_time, screenshot)

    def show_icon_summary(self, icon, summary):
        self.show_icon_summary_body(summary, icon=icon)

    def show_summary_body(self, summary, body):
        self.show_icon_summary_body(summary, body)

    def show_summary_only(self, summary):
        self.show_icon_summary_body(summary)
