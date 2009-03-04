# -*- coding: utf-8 -*-

import ldtp
import ldtputils

from time import time, sleep

from desktoptesting.deskex import NotifyOSD
from desktoptesting.check import ScreenshotCompare, PASS, FAIL

ALLOWED_OVERLAP = 14

test = NotifyOSD()

dataXml  = ldtputils.LdtpDataFileParser(datafilename)

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
    ldtp.log ('Not synchronous.', 'cause')
    ldtp.log ('Not synchronous.', 'error')    
elif (y1 + h1) - y2 > ALLOWED_OVERLAP:
    #screenshot = \
    #    ldtputils.imagecapture(x=min(x1, x2)+3, y=min(y1, y2)+3, 
    #                           resolution1=max(w1, w2)-6, 
    #                           resolution2=h2+y2-6)
    #ldtp.log (screenshot, 'screenshot')    
    ldtp.log ('Bad overlap.', 'cause')
    ldtp.log ('Bad overlap.', 'error')
    
test.exit()
