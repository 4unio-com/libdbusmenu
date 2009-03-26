# -*- coding: utf-8 -*-

import ldtp
import ldtputils
import os

from time import time, gmtime, strftime, sleep

from desktoptesting.deskex import IndicatorApplet

class IndicatorAppletTest(IndicatorApplet):
    def serverTest(self, desktop_file=None):
        self.add_server(os.path.abspath(desktop_file))
        ldtp.remap('Top Expanded Edge Panel')
        if not ldtp.objectexist('Top Expanded Edge Panel', 
                                'mnuPhonyInternetMessenger'):
            raise AssertionError("server does not appear in applet.")
