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
    def __init__(self, clean_profile=True, 
                 profile_template='',
                 credentials=''):
        self.clean_profile = clean_profile
        self.profile_template = profile_template
        self.credentials = credentials
        SingleApplicationTestSuite.__init__(self, Pidgin)

    def setup(self):
        self.application.open(
            self.clean_profile, self.profile_template, self.credentials)

    def teardown(self):
        self.application.close()

    def cleanup(self):
        #TODO: it should delete all the "My Personal Keys"
        self.application.close()
        self.application.open(
            self.clean_profile, self.profile_template, self.credentials)

