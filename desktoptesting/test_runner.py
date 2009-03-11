import ldtp, traceback
from time import time, sleep

class TestRunner:
    def setup(self):
        pass

    def teardown(self):
        pass

    def cleanup(self):
        pass

    def recover(self):
        self.teardown()
        sleep(1)
        self.setup()

    def run(self, setup_once=True):
        ldtp.log (self.__class__.__name__, 'scriptstart')
        if setup_once:
            # Set up the environment.
            self.setup()
        # Get all test* methods.
        test_attribs = filter(lambda x: x.startswith("test"), dir(self))
        test_attribs.sort()
        
        firsttest = True
        for attr in test_attribs:
            test_func = getattr(self, attr)
            if not callable(test_func): 
                continue
            starttime = time()
            ldtp.log (test_func.__doc__, 'teststart')
            if not setup_once:
                # Set up the app for each test, if requested.
                self.setup()
            if not firsttest:
                # Clean up from previous run.
                self.cleanup()
            firsttest = False
            try:
                test_func()
            except AssertionError, e:
                # The test failed.
                ldtp.log (traceback.format_exc(), 'stacktrace')
                ldtp.log (str(e), 'cause')
                ldtp.logFailures(str(e), logStatus="fail")
            except Exception, e:
                # There was an unrelated error.
                ldtp.log (traceback.format_exc(), 'stacktrace')
                ldtp.logFailures(str(e), logStatus="error")
                ldtp.logFailures(str(e), logStatus="fail")
            else:
                ldtp.log (test_func.__doc__, 'pass')
            finally:
                ldtp.log (str(time() - starttime), 'time')
                ldtp.log(test_func.__doc__, 'testend')
                if not setup_once:
                    # Tear down environment if, requested.
                    self.teardown()
        if setup_once:
            # Tear down after entire suite.
            self.teardown()
        ldtp.log (self.__class__.__name__, 'scriptend')
        ldtp.stoplog()

if __name__ == "__main__":
    from check import FileComparison, FAIL
    import sys

    ldtp.addlogger ('../conffile.ini')

    class AnAppSpecific(TestRunner):
        def setup(self):
            print >> sys.stderr, "setup"

        def teardown(self):
            print >> sys.stderr, "teardown"

        def cleanup(self):
            print >> sys.stderr, "cleanup"            
        
    class TestTest(AnAppSpecific):
        def test_01(self):
            """First Test"""
            print >> sys.stderr, 'First Test'
            fc = FileComparison('/bar', '/foo')
            if fc.perform_test() == FAIL:
                raise AssertionError, "Files differ"

        def test_02(self):
            """Second Test"""
            print >> sys.stderr, 'Second Test'
            fc = FileComparison('/etc/passwd', '/etc/fstab')
            if fc.perform_test() == FAIL:
                raise AssertionError, "Files differ"

        def test_03(self):
            """Third Test"""
            print >> sys.stderr, 'Third Test'
            fc = FileComparison('/etc/passwd', '/etc/passwd')
            if fc.perform_test() == FAIL:
                raise AssertionError, "Files differ"

    test = TestTest()
    test.run()
