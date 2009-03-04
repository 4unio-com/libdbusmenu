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

    def notify(self, summary, body="", icon=None):
	n = pynotify.Notification (summary, body, icon)
	n.show ()

    def grab_image_and_wait(self, summary):
        ldtp.waittillguiexist(summary)
        start_time = time()
        x, y, w, h = ldtp.getwindowsize(summary)
        screenshot = \
            ldtputils.imagecapture(x=x+3, y=y+3, 
                                   resolution1=w-6, 
                                   resolution2=h-6)
        ldtp.waittillguinotexist(summary)
        end_time = time() - start_time
        return (end_time, screenshot)
