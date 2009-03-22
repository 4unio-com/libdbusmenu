# -*- coding: utf-8 -*-

import ldtp
import ldtputils

from time import time, gmtime, strftime, sleep

from desktoptesting.deskex import NotifyOSD
from desktoptesting.check import ScreenshotCompare, FAIL

class NotifyOSDTest(NotifyOSD):
    def layoutTest(self, oracle=None, summary=None, body=None, icon=None):
        self.notify(summary, body, icon)
        elapsed, screeny = self.grab_image_and_wait(summary)

        checker = ScreenshotCompare(oracle, screeny)

        try:
            passed = checker.perform_test()
        except Exception, e:
            checker.calibrate()
            raise e

        if passed == FAIL:
            raise AssertionError('screenshots differ', screeny)

    def queueTest(self, oracle=None, summary=None, body=None, icon=None):
        oracles = oracle.split('|')
        summaries = summary.split('|')
        bodies = body.split('|')
        icons = icon.split('|')

        bubbles = []

        for oracle, summary, body, icons in \
                zip(oracles, summaries, bodies, icons):
            bubbles.append(_Bubble(oracle, summary, body, icons))

        for b in bubbles:
            self.notify(b.summary, b.body, b.icon)

        for b in bubbles:
            b.elapsed, b.screeny = self.grab_image_and_wait(b.summary)
            
        for b in bubbles:
            testcheck = ScreenshotCompare(b.oracle, b.screeny)

            try:
                check = testcheck.perform_test()
            except Exception, e:
                testcheck.calibrate()
                raise e

            if check == FAIL:
                raise AssertionError("screenshots differ", b.screeny)

    def synchronousTest(self, summary1=None, body1=None, icon1=None,
                        summary2=None, body2=None, icon2=None, value2=None):
        ALLOWED_OVERLAP = 14

        self.notify(summary1, body1, icon1)
        sleep(1)
        self.notify_synchronous(summary2, body2, icon2, int(value2))

        x2, y2, w2, h2 = self.get_extents(summary2, True)
        x1, y1, w1, h1 = self.get_extents(summary1)

        if w1 == -1:
            # First bubble does not exist anymore, this could mean 
            # that the second bubble did not appear synchronously.
            raise AssertionError("not synchronous")
        elif (y1 + h1) - y2 > ALLOWED_OVERLAP:
            raise AssertionError("bad overlap")

class _Bubble:
    def __init__(self, oracle, summary, body, icon):
        self.oracle = oracle
        self.summary = summary
        self.body = body
        self.icon = icon
        self.elapsed = None
        self.screeny = None
