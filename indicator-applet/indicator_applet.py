# -*- coding: utf-8 -*-

import ldtp
import ldtputils
import os

from time import time, gmtime, strftime, sleep
from desktoptesting.check import ScreenshotCompare, FAIL
from desktoptesting.test_suite.deskex import IndicatorAppletTestSuite

class IndicatorAppletTest(IndicatorAppletTestSuite):
    def serverTest(self, desktop_file=None):
        self.application.add_server(os.path.abspath(desktop_file))
        if not ldtp.objectexist(self.application.TOP_PANEL, 
                                'mnuPhonyInternetMessenger'):
            raise AssertionError("server does not appear in applet.")

    def messageTest(self, desktop_file=None, sender=None):
        self.application.add_server(os.path.abspath(desktop_file))
        self.application.show_indicator(sender)
        sleep(1)
        if not ldtp.objectexist(self.application.TOP_PANEL, 
                                'mnu' + sender.replace(' ','')):
            raise AssertionError('indicator did not appear in applet.')

    def iconChangeTest(self, desktop_file=None, sender=None):
        self.application.add_server(os.path.abspath(desktop_file))
        no_message = self.application.capture_applet_icon()
        self.application.show_indicator(sender)
        with_message = self.application.capture_applet_icon()

        checker = ScreenshotCompare(no_message, with_message)
        
        if checker.perform_test() != FAIL:
            raise AssertionError('icon did not change.')

    def displayIndicatorTest(self, desktop_file=None, sender=None):
        self.application.add_server(os.path.abspath(desktop_file))
        self.application.show_indicator(sender)
        sleep(1)
        self.application.select_indicator(sender)
        if not self.application.wait_for_indicator_display(sender):
            raise AssertionError('Indicator did not get a callback')

    def displayServerTest(self, desktop_file=None):
        self.application.add_server(os.path.abspath(desktop_file))
        sleep(1)
        ldtp.selectmenuitem(self.application.TOP_PANEL, 
                            'mnuPhonyInternetMessenger')
        if not self.application.wait_for_server_display():
            raise AssertionError('Server did not get a callback')
        
