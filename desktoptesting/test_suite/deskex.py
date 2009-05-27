"""
gnome module contains the definition of the test suites used for gnome
applications
"""
import ldtp, ooldtp
from .main import SingleApplicationTestSuite
from ..application.deskex import Application, IndicatorApplet, NotifyOSD

class IndicatorAppletTestSuite(SingleApplicationTestSuite):
    """
    Default test suite for Seahorse
    """
    APPLICATION_FACTORY = IndicatorApplet
    def setup(self):
        self.application.open()

    def teardown(self):
        self.application.close()

    def cleanup(self):
        self.application.close()

class NotifyOSDTestSuite(SingleApplicationTestSuite):
    """
    Default test suite for Seahorse
    """
    APPLICATION_FACTORY = NotifyOSD
    def setup(self):
        self.application.open()

    def teardown(self):
        self.application.close()

    def cleanup(self):
        pass
