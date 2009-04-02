from pidgin_app import Pidgin
from ConfigParser import ConfigParser
import ldtp, ooldtp, ldtputils
from time import sleep
from shutil import copytree, move
from os.path import expanduser

class PidginUseTest(Pidgin):
    def open(self):
        self.backup_config()
        copytree('./pidgin/data/purple', expanduser('~/.purple'))
        #move(expanduser('~/purple'), expanduser('~/.purple'))
        self.open_and_check_app()

    def testBasic(self):
        print 'doin test'
