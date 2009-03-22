from desktoptesting.gnome import Application
from time import time
import tempfile
import pynotify
import ldtp, ldtputils
import os

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
    test = NotifyOSD()
    test.open(False)
    test.notify("Test", "testy test", "notification-message-IM")
    test.notify_synchronous("Volume", "", 
                            "notification-audio-volume-medium", 75)
    test.exit()
