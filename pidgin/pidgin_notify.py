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
        # close all windows except buddy list
        #windows = filter(lambda x: x != self.WINDOW, self.get_all_windows())
        #while windows:
        #    for w in windows:
        #        self.close_conversation(w)
        #    windows = filter(lambda x: x != self.WINDOW, 
        #                     self.get_all_windows())
            

    def open(self):
        starttime = time()
        Pidgin.open(self)
        self.buddy = None
        ldtp.waittillguiexist(self.WINDOW)

        cp = self.credentials
        print 'gui exists'
        account_info = dict(cp.items('XMPP'))
        account_info['name'] = '%s@%s' % (account_info['username'],
                                          account_info['domain'])
                                             
        frm_buddy_list = ooldtp.context(self.WINDOW)

        print 'account connected'
        self.wait_for_account_connect(account_info['name'], 'XMPP')

        # The notify plugin only starts working after 15 seconds.
        # We use 20 here to be safe.
        print 'sleeping', 20 - (time() - starttime)
        sleep(20 - (time() - starttime))
        print 'slept'

    def click_indicator_server(self):
        objs = ldtp.getobjectlist(self.TOP_PANEL)

        for obj in objs:
            if obj.startswith('mnuPidginInternetMessenger'):
                parent = ldtp.getobjectproperty(self.TOP_PANEL, obj, 'parent')
                while parent != self.TOP_PANEL:
                    if parent == 'embindicator-applet':
                        ldtp.selectmenuitem(self.TOP_PANEL, obj)
                        return
                    parent = ldtp.getobjectproperty(self.TOP_PANEL, 
                                                    parent, 'parent')
        raise Exception('pidgin does not appear in indicator applet')
        

    def buddy_login(self):
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

    def exit(self):
        if self.buddy:
            self.buddy.disconnect()
        if not ldtp.hasstate(self.WINDOW, self.WINDOW, ldtp.state.SHOWING):
            self.click_indicator_server()
            sleep(1)
        Pidgin.exit(self)

    def testBuddyLogin(self):
        self.click_indicator_server()

        self.buddy_login()
        alias = self.credentials.get('OtherXMPP', 'alias')
        getprop = lambda x: ldtp.getobjectproperty(alias, alias, x)
        ldtp.waittillguiexist(alias)

        result = ldtp.getobjectinfo(alias, alias)

        success = result and \
            getprop('parent') == 'notify-osd' and \
            getprop('description') == 'is online'

        self.click_indicator_server()
        if not success:
            raise AssertionError, 'did not recieve a notification bubble.'
                    
    def testRecieveMessage(self, msg1='', msg2='', timeout=5):
        print 'testRecieveMessage'
        if not self.buddy:
            self.buddy_login()
            sleep(3)


        print 'clicking indicator server'
        self.click_indicator_server()
        sleep(3)

        jid = '%s@%s' % (self.credentials.get('XMPP', 'username'), 
                         self.credentials.get('XMPP', 'domain'))

        alias = self.credentials.get('OtherXMPP', 'alias')

        self.buddy.send_message(jid, '', msg1)
        sleep(2)
        self.buddy.send_message(jid, '', msg2)

        result = 1

        count = 0

        while result:
            frm_name = 'frm%s' % alias.replace(' ', '')
            if count != 0:
                frm_name += str(count)
            result = ldtp.waittillguiexist(frm_name)
            if result:
                frm = ooldtp.context(frm_name)
                getprop = frm.getobjectproperty
                if getprop(frm_name, 'parent') == 'notify-osd' and \
                        getprop(frm_name, 'description') == msg2:
                    break
            count += 1

        print 'clicking indicator server'
        self.click_indicator_server()
        sleep(1)

        if not result:
            raise AssertionError, 'did not recieve a notification bubble.'
