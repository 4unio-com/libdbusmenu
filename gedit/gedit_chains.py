# -*- coding: utf-8 -*-

import ldtp
import ldtputils

from time import time, gmtime, strftime

from desktoptesting.gnome import GEdit
from desktoptesting.check import FileComparison, FAIL
from desktoptesting.test_runner import TestRunner

class GEditChain(GEdit):
    def testASCII(self):
        "Save ASCII to file"
        self._commonTest(
            "./gedit/data/ascii.txt",
            "This is a very basic string!",
            strftime("/tmp/" + "%Y%m%d_%H%M%S" + ".txt", gmtime((time()))))

    def testUnicode(self):
        "Save Unicode to file"
        self._commonTest(
            "./gedit/data/utf8.txt",
            "This is a japanese string: 広告掲載 - ビジネス",
            strftime("/tmp/" + "%Y%m%d_%H%M%S" + ".txt", gmtime((time()))))

    def _commonTest(self, oracle, chain, test_file):
        self.write_text(chain)
        self.save(test_file)

        testcheck = FileComparison(oracle, test_file)

        if testcheck.perform_test() == FAIL:
            raise AssertionError, "Files differ"

gedit_chains_test = GEditChain()
gedit_chains_test.run()
