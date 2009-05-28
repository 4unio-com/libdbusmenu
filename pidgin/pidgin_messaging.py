from desktoptesting.test_suite.pidgin import PidginTestSuite
from desktoptesting.test_suite.main import SingleApplicationTestSuite
from desktoptesting.application.pidgin import Pidgin
from ConfigParser import ConfigParser
import ldtp, ooldtp, ldtputils
from time import sleep, time
from shutil import copytree, move
from os.path import expanduser

class PidginUseApp(Pidgin):
    def open(self, clean_profile=True, profile_template='', credentials=''):
        Pidgin.open(self, clean_profile, profile_template, credentials)
        self.buddy_login()
        self.wait_for_account_connect(self.get_account_name('XMPP'), 'XMPP')
        self.wait_for_buddy(self.get_account_alias('OtherXMPP'))
    
    def close(self):
        self.buddy.disconnect()
        Pidgin.close(self)

class PidginUseTest(PidginTestSuite):
    APPLICATION_FACTORY = PidginUseApp
    def __init__(self, clean_profile=True, profile_template='', credentials=''):
        print 'init', clean_profile, profile_template, credentials
        PidginTestSuite.__init__(self, clean_profile, profile_template, credentials)
    def cleanup(self):
        return

    def testSendMessage(self, msg=''):
        buddy_alias = self.application.get_account_alias('OtherXMPP')

        self.application.send_message(buddy_alias, msg)

        self.application.buddy.wait_for_message(body=msg, timeout=5)

    def testRecieveMessage(self, msg='', timeout=5):
        buddy_alias = self.application.get_account_alias('OtherXMPP')

        prev_log = self.application.get_conversation_log(buddy_alias)

        self.application.buddy.send_message(self.application.get_account_name('XMPP'), '', msg)
        
        for i in xrange(timeout):
            log = self.application.get_conversation_log(buddy_alias)
            recent_ims = log[len(prev_log):].split('\n')
            for im in recent_ims:
                if im.split(buddy_alias+': ')[-1] == msg:
                    return
            sleep(1)
        
        raise AssertionError("Did not recieve matching message", 
                             ldtputils.imagecapture())

