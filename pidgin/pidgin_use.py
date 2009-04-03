from pidgin_app import Pidgin
from ConfigParser import ConfigParser
import ldtp, ooldtp, ldtputils
from time import sleep, time
from shutil import copytree, move
from os.path import expanduser
from xmpp_utils import Buddy

class PidginUseTest(Pidgin):
    def open(self):
        self.backup_config()
        copytree('./pidgin/data/purple', expanduser('~/.purple'))
        self.open_and_check_app()

    def testSendMessage(self, credentials=None, msg='', connect_timeout=5):
        cp = ConfigParser()
        cp.read(credentials)

        buddy_info = dict(cp.items('OtherXMPP'))

        buddy_info['alias'] = buddy_info.get(
            'alias', '%s@%s' % (buddy_info['username'], buddy_info['domain']))

        ldtp.waittillguiexist(self.WINDOW)

        buddy = Buddy('%s@%s' % (buddy_info['username'], buddy_info['domain']),
                      buddy_info['password'])
        buddy.connect()

        account_info = dict(cp.items('XMPP'))
        account_info['name'] = '%s@%s' % (account_info['username'],
                                          account_info['domain'])
                                             
        frm_buddy_list = ooldtp.context(self.WINDOW)

        self.wait_for_account_connect(account_info['name'], 'XMPP')

        self.send_message(buddy_info['alias'], msg)

        buddy.wait_for_message(body=msg, timeout=5)

        buddy.disconnect()
