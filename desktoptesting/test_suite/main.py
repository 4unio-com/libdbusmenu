"""
test_suite module contains the definition of the TestSuite class that
must be used by all test suites written for the desktoptesting package
"""
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
    """
    def __init__(self, application_factory):
        self.application = application_factory()

    def cleanup(self):
        self.application.set_name(self.WINDOW)
        self.application.set_close_type(self.CLOSE_TYPE)
        self.application.set_close_name(self.CLOSE_NAME)
