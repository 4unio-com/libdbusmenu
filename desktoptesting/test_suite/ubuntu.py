"""
ubuntu module contains the definition of the test suites used for ubuntu
applications
"""
from .main import SingleApplicationTestSuite
from ..application.ubuntu import UbuntuMenu, UpdateManager

class UbuntuMenuTestSuite(SingleApplicationTestSuite):
    def __init__(self):
        SingleApplicationTestSuite.__init__(self, UbuntuMenu)

    def teardown(self):
        self.cleanup() 

    def cleanup(self):
        self.application.close()
        SingleApplicationTestSuite.cleanup(self)


class UpdateManagerTestSuite(SingleApplicationTestSuite):
    def __init__(self):
        SingleApplicationTestSuite.__init__(self, UpdateManager)
