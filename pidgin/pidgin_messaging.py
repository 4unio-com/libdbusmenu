from pidgin_app import Pidgin
from ConfigParser import ConfigParser
import ldtp, ooldtp, ldtputils
from time import sleep, time
from shutil import copytree, move
from os.path import expanduser
from xmpp_utils import Buddy

class PidginUseTest(Pidgin):
    def cleanup(self):
        return
        # close all windows except buddy list
        #windows = filter(lambda x: x != self.WINDOW, self.get_all_windows())
        #while windows:
        #    for w in windows:
        #        self.close_conversation(w)
        #    windows = filter(lambda x: x != self.WINDOW, 
        #                     self.get_all_windows())
            

    def open(self):
        Pidgin.open(self)
        cp = self.credentials

        buddy_info = dict(cp.items('OtherXMPP'))

        buddy_info['alias'] = buddy_info.get(
            'alias', '%s@%s' % (buddy_info['username'], buddy_info['domain']))


        self.buddy = \
            Buddy('%s@%s' % (buddy_info['username'], buddy_info['domain']),
                  buddy_info['password'])
        print 'connecting buddy'
        self.buddy.connect()
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
        
    def exit(self):
        self.buddy.disconnect()
        Pidgin.exit(self)

    def testSendMessage(self, msg=''):
        buddy_alias = self.credentials.get('OtherXMPP', 'alias')

        print 'sending message'
        self.send_message(buddy_alias, msg)

        self.buddy.wait_for_message(body=msg, timeout=5)

    def testRecieveMessage(self, msg='', timeout=5):
        jid = '%s@%s' % (self.credentials.get('XMPP', 'username'), 
                         self.credentials.get('XMPP', 'domain'))

        buddy_alias = self.credentials.get('OtherXMPP', 'alias')

        prev_log = self.get_conversation_log(buddy_alias)

        self.buddy.send_message(jid, '', msg)
        
        for i in xrange(timeout):
            log = self.get_conversation_log(buddy_alias)
            recent_ims = log[len(prev_log):].split('\n')
            for im in recent_ims:
                if im.split(buddy_alias+': ')[-1] == msg:
                    return
            sleep(1)
        
        raise AssertionError("Did not recieve matching message", 
                             ldtputils.imagecapture())

