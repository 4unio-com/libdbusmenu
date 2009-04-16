from pidgin_app import Pidgin
from ConfigParser import ConfigParser
import ldtp, ooldtp, ldtputils
from time import sleep, time
from shutil import copytree, move
from os.path import expanduser
from xmpp_utils import Buddy

class PidginNotifyTest(Pidgin):
    def cleanup(self):
        return

    def open(self):
        starttime = time()
        Pidgin.open(self)
        self.buddy = None
        ldtp.waittillguiexist(self.WINDOW)

        cp = self.credentials
        account_info = dict(cp.items('XMPP'))
        account_info['name'] = '%s@%s' % (account_info['username'],
                                          account_info['domain'])
                                             
        frm_buddy_list = ooldtp.context(self.WINDOW)

        self.wait_for_account_connect(account_info['name'], 'XMPP')

        # The notify plugin only starts working after 15 seconds.
        # We use 20 here to be safe.
        sleep(20 - (time() - starttime))

    def click_in_indicator(self, name):
        objs = ldtp.getobjectlist(self.TOP_PANEL)

        for obj in objs:
            if obj.startswith(name):
                if self.is_in_indicator(obj):
                    ldtp.selectmenuitem(self.TOP_PANEL, obj)
                    return

        raise Exception('pidgin does not appear in indicator applet')

    def is_in_indicator(self, obj):
        parent = ldtp.getobjectproperty(self.TOP_PANEL, obj, 'parent')
        while parent != self.TOP_PANEL:
            if parent == 'embindicator-applet':
                return True
            parent = ldtp.getobjectproperty(self.TOP_PANEL, 
                                            parent, 'parent')
        return False
        
    def testIndicatorServer(self):
        flipflop = []
        flipflop.append(
            ldtp.hasstate(self.WINDOW, self.WINDOW, ldtp.state.SHOWING))

        self.click_in_indicator('mnuPidginInternetMessenger')
        sleep(2)

        flipflop.append(
            ldtp.hasstate(self.WINDOW, self.WINDOW, ldtp.state.SHOWING))

        self.click_in_indicator('mnuPidginInternetMessenger')
        sleep(2)
            
        flipflop.append(
            ldtp.hasstate(self.WINDOW, self.WINDOW, ldtp.state.SHOWING))

        if flipflop not in ([1, 0, 1], [0, 1, 0]):
            raise AssertionError, \
                'indicator server menu item did not show/hide the buddy list'

    def buddy_login(self):
        cp = self.credentials

        buddy_info = dict(cp.items('OtherXMPP'))
        buddy_info['alias'] = buddy_info.get(
            'alias', '%s@%s' % (buddy_info['username'], buddy_info['domain']))


        self.buddy = \
            Buddy('%s@%s' % (buddy_info['username'], buddy_info['domain']),
                  buddy_info['password'])
        self.buddy.connect()

    def exit(self):
        if self.buddy:
            self.buddy.disconnect()
        if not ldtp.hasstate(self.WINDOW, self.WINDOW, ldtp.state.SHOWING):
            self.click_in_indicator('mnuPidginInternetMessenger')
            sleep(1)
        Pidgin.exit(self)

    def testBuddyLogin(self):
        self.buddy_login()
        alias = self.credentials.get('OtherXMPP', 'alias')

        result = 1
        count = 0

        while result:
            frm_name = 'dlg%s' % alias.replace(' ', '')
            if count != 0:
                frm_name += str(count)
            result = ldtp.waittillguiexist(frm_name)
            if result:
                frm = ooldtp.context(frm_name)
                if self.is_bubble(frm_name) and \
                        self.bubble_body(frm_name) == 'is online':
                    break
            count += 1

        if not result:
            raise AssertionError, 'did not recieve a notification bubble.'

    def is_bubble(self, frm_name):
        return ldtp.getobjectproperty(
            frm_name, frm_name, 'parent') == 'notify-osd'        
            
    def bubble_body(self, frm_name):
        return ldtp.getobjectproperty(frm_name, frm_name, 'description')
        
    def testRecieveMessage(self, msg1='', msg2='', msg3='', timeout=5):
        if not self.buddy:
            self.buddy_login()
            sleep(1)

        jid = '%s@%s' % (self.credentials.get('XMPP', 'username'), 
                         self.credentials.get('XMPP', 'domain'))

        alias = self.credentials.get('OtherXMPP', 'alias')

        #https://bugs.launchpad.net/ubuntu/+source/pidgin-libnotify/+bug/362248
        ldtp.waittillguinotexist('dlg%s' % alias.replace(' ', ''))

        self.buddy.send_message(jid, '', msg1)
        sleep(2)
        self.buddy.send_message(jid, '', msg2)

        result = 1
        count = 0
        frm_name = ''

        while result:
            frm_name = 'dlg%s' % alias.replace(' ', '')
            if count != 0:
                frm_name += str(count)
            result = ldtp.waittillguiexist(frm_name)
            if result:
                if self.is_bubble(frm_name) and \
                        self.bubble_body(frm_name) == msg2:
                    break
            count += 1

        if not result:
            raise AssertionError, \
                'did not recieve a message notification bubble.'

        self.buddy.send_message(jid, '', msg3)

        for i in xrange(timeout):
            ldtp.remap(frm_name)
            try:
                if self.bubble_body(frm_name) == '%s\n%s' % (msg2, msg3):
                    return
            except ldtp.LdtpExecutionError:
                screeny = ldtputils.imagecapture()
                raise AssertionError(
                        'notification for second message does not exist',
                        screeny)
            sleep(1)

        raise AssertionError, 'second message was not appended'
