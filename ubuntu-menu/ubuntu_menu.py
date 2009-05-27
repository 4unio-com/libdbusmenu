from desktoptesting.test_suite.ubuntu import UbuntuMenuTestSuite

class UbuntuMenuTest(UbuntuMenuTestSuite):
       
    def testOpenMenu(self, menuitem=None, windowname=None, closetype=None, closename=None):
        self.application.set_name(windowname)
        self.application.set_close_type(closetype)
        self.application.set_close_name(closename)
        self.application.open_and_check_menu_item(menuitem)
        
if __name__ == "__main__":
    ubuntu_menu_test = UbuntuMenuTest()
    ubuntu_menu_test.run()
