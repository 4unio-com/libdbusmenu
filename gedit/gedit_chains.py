# -*- coding: utf-8 -*-
from time import time, gmtime, strftime

from desktoptesting.test_suite import GEditTestSuite
from desktoptesting.check import FileComparison, FAIL

class GEditChain(GEditTestSuite):
    def testChain(self, oracle=None, chain=None):
        test_file = strftime(
            "/tmp/" + "%Y%m%d_%H%M%S" + ".txt", gmtime((time())))

        self.application.write_text(chain)
        self.application.save(test_file)

        testcheck = FileComparison(oracle, test_file)

        if testcheck.perform_test() == FAIL:
            raise AssertionError, "Files differ"

if __name__ == "__main__":
    gedit_chains_test = GEditChain()
    gedit_chains_test.run()
