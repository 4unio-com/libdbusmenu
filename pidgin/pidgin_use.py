from pidgin_app import Pidgin
from ConfigParser import ConfigParser
import ldtp, ooldtp, ldtputils
from time import sleep, time
from shutil import copytree, move
from os.path import expanduser
from xmpp_utils import Buddy

class PidginUseTest(Pidgin):
    def testSendMessage(self, msg='', connect_timeout=5):
        cp = self.credentials

        buddy_info = dict(cp.items('OtherXMPP'))

        buddy_info['alias'] = buddy_info.get(
            'alias', '%s@%s' % (buddy_info['username'], buddy_info['domain']))


        buddy = Buddy('%s@%s' % (buddy_info['username'], buddy_info['domain']),
                      buddy_info['password'])
        print 'connecting buddy'
        buddy.connect()
        print 'connected buddy'

        ldtp.waittillguiexist(self.WINDOW)

        print 'gui exists'
        account_info = dict(cp.items('XMPP'))
        account_info['name'] = '%s@%s' % (account_info['username'],
                                          account_info['domain'])
                                             
        frm_buddy_list = ooldtp.context(self.WINDOW)

        print 'account connected'
        self.wait_for_account_connect(account_info['name'], 'XMPP')

        print 'wait for buddy'
        self.wait_for_buddy(buddy_info['alias'])

        print 'sending message'
        self.send_message(buddy_info['alias'], msg)

        buddy.wait_for_message(body=msg, timeout=5)

        buddy.disconnect()
