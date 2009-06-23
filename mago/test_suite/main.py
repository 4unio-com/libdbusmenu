"""
test_suite module contains the definition of the TestSuite class that
must be used by all test suites written for the mago package
"""
from ..application.main import Application

class TestSuite:
    """
    TestSuite that implements all the test suite methods desired in a
    test suite
    """
    def setup(self):
        pass

    def teardown(self):
        pass

    def cleanup(self):
        pass


class SingleApplicationTestSuite(TestSuite):
    """
    Test suite intended to make sure that a single application is
    running

    APPLICATION_FACTORY: A class attribute that stores the factory for an
    Application instance.
    """
    APPLICATION_FACTORY = Application
    def __init__(self):
        self.application = self.APPLICATION_FACTORY()

    def cleanup(self):
        self.application.set_name(self.application.WINDOW)
        self.application.set_close_type(self.application.CLOSE_TYPE)
        self.application.set_close_name(self.application.CLOSE_NAME)
