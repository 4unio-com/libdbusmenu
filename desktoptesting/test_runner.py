import ldtp, traceback
from time import time, sleep


class TestSuite:
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
