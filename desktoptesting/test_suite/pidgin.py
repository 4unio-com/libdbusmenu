"""
gnome module contains the definition of the test suites used for gnome
applications
"""
import ldtp, ooldtp
from .main import SingleApplicationTestSuite
from ..application.gnome import Application
from ..application.pidgin import Pidgin

class PidginTestSuite(SingleApplicationTestSuite):
    """
    Default test suite for Pidgin
    """
    APPLICATION_FACTORY = Pidgin
    def __init__(self, **kwargs):
        self.app_args = kwargs
        SingleApplicationTestSuite.__init__(self)

    def setup(self):
        self.application.open(**self.app_args)

    def teardown(self):
        self.application.close()

    def cleanup(self):
        #TODO: it should delete all the "My Personal Keys"
        self.application.close()
        self.application.open(**self.app_args)

