# -*- coding: utf-8 -*-

import ldtp
import ldtputils
import os

from time import time, gmtime, strftime, sleep
from desktoptesting.check import ScreenshotCompare, FAIL
from desktoptesting.deskex import IndicatorApplet, IA_TOPLEVEL, TOP_PANEL

class IndicatorAppletTest(IndicatorApplet):
    def serverTest(self, desktop_file=None):
        self.add_server(os.path.abspath(desktop_file))
        if not ldtp.objectexist(TOP_PANEL, 'mnuPhonyInternetMessenger'):
            raise AssertionError("server does not appear in applet.")

    def messageTest(self, desktop_file=None, sender=None):
        self.add_server(os.path.abspath(desktop_file))
        self.show_indicator(sender)
        if not ldtp.objectexist(TOP_PANEL, 'mnu' + sender.replace(' ','')):
            raise AssertionError('indicator did not appear in applet.')

    def iconChangeTest(self, desktop_file=None, sender=None):
        self.add_server(os.path.abspath(desktop_file))
        no_message = self.capture_applet_icon()
        self.show_indicator(sender)
        with_message = self.capture_applet_icon()

        checker = ScreenshotCompare(no_message, with_message)
        
        if checker.perform_test() != FAIL:
            raise AssertionError('icon did not change.')

