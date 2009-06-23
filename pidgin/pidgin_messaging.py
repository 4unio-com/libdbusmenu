from mago.test_suite.pidgin import PidginTestSuite
from mago.application.pidgin import Pidgin, AccountInfo
from ConfigParser import ConfigParser
import ldtp, ooldtp, ldtputils
from time import sleep, time
from shutil import copytree, move
from os.path import expanduser

class PidginUseApp(Pidgin):
    def open(self, profile_template='', credentials='',
             me_account='', buddy_account=''):
        self.me_account = AccountInfo(me_account, credentials)
        self.buddy_account = AccountInfo(buddy_account, credentials)

        self.backup_config()
        self.generate_profile(profile_template, self.me_account.template_args)

        Pidgin.open(self, False, credentials)

        print 'wait_for_account_connect?'
        self.wait_for_account_connect(self.me_account)
        print 'account connect'
        self.buddy_login(self.buddy_account)
        self.wait_for_buddy(self.buddy_account.alias)
    
    def close(self):
        self.buddy.disconnect()
        Pidgin.close(self)

class PidginUseTest(PidginTestSuite):
    APPLICATION_FACTORY = PidginUseApp
    def cleanup(self):
        return

    def testSendMessage(self, msg=''):
        buddy_alias = self.application.buddy_account.alias

        self.application.send_message(
            self.application.buddy_account.alias, msg)
        self.application.buddy.wait_for_message(body=msg, timeout=5)

    def testRecieveMessage(self, msg='', timeout=5):
        buddy_alias = self.application.buddy_account.alias

        prev_log = self.application.get_conversation_log(buddy_alias)

        self.application.buddy.send_message(
            self.application.me_account.username, msg)
        
        for i in xrange(timeout):
            log = self.application.get_conversation_log(
                buddy_alias)
            recent_ims = log[len(prev_log):].split('\n')
            for im in recent_ims:
                if im.split(
                    buddy_alias+': ')[-1] == msg:
                    return
            sleep(1)
        
        raise AssertionError("Did not recieve matching message", 
                             ldtputils.imagecapture())

