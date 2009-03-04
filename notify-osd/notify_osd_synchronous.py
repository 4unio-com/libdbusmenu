# -*- coding: utf-8 -*-

import ldtp
import ldtputils

from time import time, sleep

from desktoptesting.deskex import NotifyOSD
from desktoptesting.check import ScreenshotCompare, PASS, FAIL

ALLOWED_OVERLAP = 14

test = NotifyOSD()

dataXml  = ldtputils.LdtpDataFileParser(datafilename)

start_time = time()

test.open(False)

test.notify(
    dataXml.gettagvalue("summary1")[0],
    dataXml.gettagvalue("body1")[0],
    dataXml.gettagvalue("icon1")[0])

sleep(1)

test.notify_synchronous(
    dataXml.gettagvalue("summary2")[0],
    dataXml.gettagvalue("body2")[0],
    dataXml.gettagvalue("icon2")[0],
    int(dataXml.gettagvalue("value2")[0]))

x2, y2, w2, h2 = test.get_extents(dataXml.gettagvalue("summary2")[0], True)
x1, y1, w1, h1 = test.get_extents(dataXml.gettagvalue("summary1")[0])

if w1 == -1:
    # First bubble does not exist anymore, this could mean that the second
    # bubble did not appear synchronously.
    ldtp.logFailures ("Not synchronous")
    ldtp.logFailures ("Not synchronous", False, "fail") 
elif (y1 + h1) - y2 > ALLOWED_OVERLAP:
    ldtp.logFailures ("Bad overlap")
    ldtp.logFailures ("Bad overlap", False, "fail") 
    
test.exit()

ldtp.log (str(time() - start_time), 'time')
