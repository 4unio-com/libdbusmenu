# -*- coding: utf-8 -*-

import ldtp
import ldtputils
import os

from time import time, gmtime, strftime

from desktoptesting.deskex import NotifyOSD
from desktoptesting.check import ScreenshotCompare, PASS, FAIL

class Bubble:
    def __init__(self, oracle, summary, body, icon):
        self.oracle = oracle
        self.summary = summary
        self.body = body
        self.icon = icon
        self.elapsed = None
        self.screeny = None

start_time = time()

test = NotifyOSD()

test.open(False)

dataXml  = ldtputils.LdtpDataFileParser(datafilename)

bubbles = []

for bubble in dataXml.gettagvalue("bubble"):
    data_file = ldtputils.LdtpDataFileParser(
        os.path.join(os.path.dirname(datafilename), bubble))
    b = Bubble(data_file.gettagvalue("oracle")[0],
               data_file.gettagvalue("summary")[0],
               data_file.gettagvalue("body")[0],
               data_file.gettagvalue("icon")[0])
    bubbles.append(b)

for b in bubbles:
    test.notify(b.summary, b.body, b.icon)

for b in bubbles:
    b.elapsed, b.screeny = test.grab_image_and_wait(b.summary)

status = PASS

for b in bubbles:
    testcheck = ScreenshotCompare(b.oracle, b.screeny)
    check = testcheck.perform_test()
    if check == FAIL:
        status = FAIL

if status == FAIL:
    ldtp.log ('Screenshots differ.', 'cause')
    ldtp.log ('Screenshots differ.', 'error')
        
test.exit()

ldtp.log (str(time() - start_time), 'time')
