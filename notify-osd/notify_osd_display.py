# -*- coding: utf-8 -*-

import ldtp
import ldtputils

import shutil, os

from desktoptesting.deskex import NotifyOSD
from desktoptesting.check import ScreenshotCompare, PASS, FAIL

test = NotifyOSD()

dataXml  = ldtputils.LdtpDataFileParser(datafilename)

oracle = dataXml.gettagvalue("oracle")[0]
summary = dataXml.gettagvalue("summary")[0]
body = dataXml.gettagvalue("body")[0]
icon = dataXml.gettagvalue("icon")[0]

test.open(False)
test.notify(summary, body, icon)
elapsed, screeny = test.grab_image_and_wait(summary)
    
testcheck = ScreenshotCompare(oracle, screeny)
check = testcheck.perform_test()

if check == FAIL:
    shutil.copy(screeny, "/tmp/ldtp-screenshots")
    newscreeny = os.path.join("/tmp/ldtp-screenshots", 
                              os.path.basename(screeny))
    ldtp.log (newscreeny, "screenshot")
    ldtp.logFailures ("Screenshots differ", False)
    ldtp.logFailures ("Screenshots differ", False, "fail") 

test.exit()

ldtp.log (str(elapsed), 'time')
