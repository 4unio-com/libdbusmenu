"""
ubuntu module contains the definition of the test suites used for ubuntu
applications
"""
from .main import SingleApplicationTestSuite
from ..application.ubuntu import UbuntuMenu, UpdateManager

class UbuntuMenuTestSuite(SingleApplicationTestSuite):
    APPLICATION_FACTORY = UbuntuMenu
    def teardown(self):
        self.cleanup() 

    def cleanup(self):
        self.application.close()
        SingleApplicationTestSuite.cleanup(self)


class UpdateManagerTestSuite(SingleApplicationTestSuite):
    APPLICATION_FACTORY = UpdateManager
