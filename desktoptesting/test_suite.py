"""
test_suite module contains the definition of the TestSuite class that
must be used by all test suites written for the desktoptesting package
"""
import ldtp, ooldtp
from gnome import Application, Seahorse, GEdit
from ubuntu import UbuntuMenu, UpdateManager

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


class SeahorseTestSuite(SingleApplicationTestSuite):
    """
    Default test suite for Seahorse
    """
    def __init__(self):
        SingleApplicationTestSuite.__init__(self, Seahorse)

    def setup(self):
        self.application.open()

    def teardown(self):
        self.application.close()

    def cleanup(self):
        #TODO: it should delete all the "My Personal Keys"
        pass


class GEditTestSuite(SingleApplicationTestSuite):
    """
    Default test suite for GEdit
    """
    def __init__(self):
        SingleApplicationTestSuite.__init__(self, GEdit)

    def setup(self):
        self.application.open()

    def teardown(self):
        self.application.close()

    def cleanup(self):
        # Exit using the Quit menu 
        try:
            try:
                gedit = ooldtp.context(self.application.name)
                quit_menu = gedit.getchild(self.application.MNU_CLOSE)
            except ldtp.LdtpExecutionError:
                raise ldtp.LdtpExecutionError, "The quit menu was not found."
            quit_menu.selectmenuitem()
        except ldtp.LdtpExecutionError:
            raise ldtp.LdtpExecutionError, "Mmm, something went wrong when closing the application."

        result = ldtp.waittillguiexist(self.application.QUESTION_DLG,
                                       guiTimeOut = 2)

        if result == 1:
            question_dialog = ooldtp.context(self.application.QUESTION_DLG)
            question_dlg_btn_close = question_dialog.getchild(self.application.QUESTION_DLG_BTN_CLOSE)
            question_dlg_btn_close.click()
        
        try:
            gedit = ooldtp.context(self.application.name)
            new_menu = gedit.getchild(self.application.MNU_NEW)
        except ldtp.LdtpExecutionError:
            raise ldtp.LdtpExecutionError, "The new menu was not found."
        new_menu.selectmenuitem()

        result = ldtp.waittillguiexist(
            self.application.name, self.application.TXT_FIELD)
        if result != 1:
            raise ldtp.LdtpExecutionError, "Failed to set up new document."
        

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
