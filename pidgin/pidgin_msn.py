from desktoptesting.pidgin import Pidgin
from ConfigParser import ConfigParser
import ldtp, ooldtp, ldtputils
from time import sleep, time
from shutil import copytree, move
from os.path import expanduser

class PidginMSNUseTest(Pidgin):
    def cleanup(self):
        return            

    def open(self):
        Pidgin.open(self)
        self.buddy_msn_login()
        self.wait_for_account_connect(self.get_account_name('MSN'), 'MSN')
        self.wait_for_buddy(self.get_account_alias('OtherMSN'))
    
    def exit(self):
        #TODO: The logout method in pymsn is causing the whole suite to exit
        # as it conflicts with the transport protocol of LDTP. Any ideas?
        #self.buddy.disconnect()
        Pidgin.exit(self)

    def testSendMessage(self, msg=''):
        buddy_account = self.get_account_name('OtherMSN')
        my_account = self.get_account_name('MSN')

        print 'sending message'
        self.send_message(buddy_account, msg)

        self.buddy.wait_for_message(my_account, msg, timeout=5)

    def testRecieveMessage(self, msg='', timeout=5):
        buddy_alias = self.get_account_alias('OtherMSN')

        prev_log = self.get_conversation_log(buddy_alias)

        self.buddy.send_message(self.get_account_name('MSN'), msg)
        
        for i in xrange(timeout):
            log = self.get_conversation_log(buddy_alias)
            recent_ims = log[len(prev_log):].split('\n')
            for im in recent_ims:
                if im.split(buddy_alias+': ')[-1] == msg:
                    return
            sleep(1)
        
        raise AssertionError("Did not recieve matching message", 
                             ldtputils.imagecapture())

