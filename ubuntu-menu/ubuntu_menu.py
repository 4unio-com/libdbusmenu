import ldtp 
import ldtputils
from time import time 

from desktoptesting.ubuntu import UbuntuMenu

class UbuntuMenuTest(UbuntuMenu):
       
    def testOpenMenu(self, menuitem=None, windowname=None, closetype=None, closename=None):
        self.set_name(windowname)
        self.set_close_type(closetype)
        self.set_close_name(closename)
        self.open_and_check_menu_item(menuitem)
        
if __name__ == "__main__":
    ubuntu_menu_test = UbuntuMenuTest()
    ubuntu_menu_test.run()


