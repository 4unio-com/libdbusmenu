from desktoptesting.gnome import Application
from shutil import move, rmtree
import os

class Pidgin(Application):
    WINDOW = "frmBuddyList"
    LAUNCHER = "pidgin"

    def setup(self):
        self.open()

    def teardown(self):
        self.exit()

    def cleanup(self):
        #TODO: it should delete all the "My Personal Keys"
        self.exit()
        self.open()

    def open(self, clean_profile=True):
        self._clean_profile = clean_profile
        try:
            move(os.path.expanduser('~/.purple'), 
                 os.path.expanduser('~/.purple.bak'))
        except IOError:
            raise

        Application.open_and_check_app(self)

    def exit(self):
        try:
            rmtree('~/.purple')
        except OSError:
            pass
        
        try:
            move(os.path.expanduser('~/.purple.bak'), 
                 os.path.expanduser('~/.purple'))
        except IOError:
            pass
        
        Application.exit(self)
        
