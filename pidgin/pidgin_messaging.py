from desktoptesting.pidgin import Pidgin
from ConfigParser import ConfigParser
import ldtp, ooldtp, ldtputils
from time import sleep, time
from shutil import copytree, move
from os.path import expanduser

class PidginUseTest(Pidgin):
    def cleanup(self):
        return            

    def open(self):
        Pidgin.open(self)
        self.buddy_login()
        self.wait_for_account_connect(self.get_account_name('XMPP'), 'XMPP')
        self.wait_for_buddy(self.get_account_alias('OtherXMPP'))
    
    def exit(self):
        self.buddy.disconnect()
        Pidgin.exit(self)

    def testSendMessage(self, msg=''):
        buddy_alias = self.get_account_alias('OtherXMPP')

        print 'sending message'
        self.send_message(buddy_alias, msg)

        self.buddy.wait_for_message(body=msg, timeout=5)

    def testRecieveMessage(self, msg='', timeout=5):
        buddy_alias = self.get_account_alias('OtherXMPP')

        prev_log = self.get_conversation_log(buddy_alias)

        self.buddy.send_message(self.get_account_name('XMPP'), '', msg)
        
        for i in xrange(timeout):
            log = self.get_conversation_log(buddy_alias)
            recent_ims = log[len(prev_log):].split('\n')
            for im in recent_ims:
                if im.split(buddy_alias+': ')[-1] == msg:
                    return
            sleep(1)
        
        raise AssertionError("Did not recieve matching message", 
                             ldtputils.imagecapture())

