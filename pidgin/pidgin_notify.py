from desktoptesting.pidgin import Pidgin
from ConfigParser import ConfigParser
import ldtp, ooldtp, ldtputils
from time import sleep, time
from shutil import copytree, move
from os.path import expanduser

class PidginNotifyTest(Pidgin):
    MNU_INDICATOR_SERVER = "mnuPidginInternetMessenger"
    EMB_INDICATOR_APPLET = "embindicator-applet"
    def cleanup(self):
        alias = self.get_account_alias('OtherXMPP')
        if ldtp.guiexist('frm%s' % alias.replace(' ', '')):
            self.close_conversation('frm%s' % alias.replace(' ', ''))

    def open(self):
        Pidgin.open(self)
        self.wait_for_account_connect(self.get_account_name('XMPP'), 'XMPP')

        # The notify plugin only starts working after 15 seconds.
        # We start waiting from now to be safe.
        sleep(15)

    def exit(self):
        if self.buddy:
            self.buddy.disconnect()

        if not ldtp.hasstate(self.WINDOW, self.WINDOW, ldtp.state.SHOWING):
            self._click_in_indicator(self.MNU_INDICATOR_SERVER)
            sleep(1)

        Pidgin.exit(self)

    def _click_in_indicator(self, name):
        objs = ldtp.getobjectlist(self.TOP_PANEL)

        for obj in objs:
            if obj.startswith(name):
                if self._is_in_indicator(obj):
                    ldtp.selectmenuitem(self.TOP_PANEL, obj)
                    return

        raise Exception('%s does not appear in indicator applet' % name)

    def _is_in_indicator(self, obj):
        parent = ldtp.getobjectproperty(self.TOP_PANEL, obj, 'parent')
        while parent != self.TOP_PANEL:
            if parent == self.EMB_INDICATOR_APPLET:
                return True
            parent = ldtp.getobjectproperty(self.TOP_PANEL, 
                                            parent, 'parent')
        return False
        
    def _is_bubble(self, frm_name):
        return ldtp.getobjectproperty(
            frm_name, frm_name, 'parent') == 'notify-osd'        
            
    def _bubble_body(self, frm_name):
        return ldtp.getobjectproperty(frm_name, frm_name, 'description')
        
    def _bubble_name_from_alias(self, name):
        return 'dlg%s' % name.replace(' ', '')        

    def testIndicatorServer(self):
        flipflop = []
        flipflop.append(
            ldtp.hasstate(self.WINDOW, self.WINDOW, ldtp.state.SHOWING))

        self._click_in_indicator(self.MNU_INDICATOR_SERVER)
        sleep(2)

        flipflop.append(
            ldtp.hasstate(self.WINDOW, self.WINDOW, ldtp.state.SHOWING))

        self._click_in_indicator(self.MNU_INDICATOR_SERVER)
        sleep(2)
            
        flipflop.append(
            ldtp.hasstate(self.WINDOW, self.WINDOW, ldtp.state.SHOWING))

        if flipflop not in ([1, 0, 1], [0, 1, 0]):
            raise AssertionError, \
                'indicator server menu item did not show/hide the buddy list'

    def testBuddyLogin(self):
        self.buddy_login()
        alias = self.get_account_alias('OtherXMPP')

        result = 1
        count = 0
        frm_name = ''

        while result:
            frm_name = self._bubble_name_from_alias(alias)
            if count != 0:
                frm_name += str(count)
            result = ldtp.waittillguiexist(frm_name)
            if result:
                frm = ooldtp.context(frm_name)
                if self._is_bubble(frm_name) and \
                        self._bubble_body(frm_name) == 'is online':
                    break
            count += 1

        if not result:
            raise AssertionError, 'did not recieve a notification bubble.'
        
        ldtp.remap(self.TOP_PANEL)
        try:
            self._click_in_indicator('mnu%s' % alias.replace(' ', ''))
        except Exception, e:
            raise AssertionError(e[-1])
        
        print 'success'
        result = ldtp.waittillguiexist('frm%s' % alias.replace(' ', ''))
        
        if not result:
            AssertionError, \
                'clicking on buddy indicator did not bring up chat dialog'

    def testRecieveMessageAppend(self, msg1='', msg2='', msg3='', timeout=5):
        if not self.buddy:
            self.buddy_login()
            sleep(1)

        jid = self.get_account_name('XMPP')

        alias = self.get_account_alias('OtherXMPP')

        #https://bugs.launchpad.net/ubuntu/+source/pidgin-libnotify/+bug/362248
        ldtp.waittillguinotexist(self._bubble_name_from_alias(alias))

        self.buddy.send_message(jid, '', msg1)
        sleep(2)
        self.buddy.send_message(jid, '', msg2)

        result = 1
        count = 0
        frm_name = ''

        while result:
            frm_name = self._bubble_name_from_alias(alias)
            if count != 0:
                frm_name += str(count)
            result = ldtp.waittillguiexist(frm_name)
            if result:
                if self._is_bubble(frm_name) and \
                        self._bubble_body(frm_name) == msg2:
                    break
            count += 1

        if not result:
            raise AssertionError, \
                'did not recieve a message notification bubble.'

        self.buddy.send_message(jid, '', msg3)

        for i in xrange(timeout):
            ldtp.remap(frm_name)
            try:
                if self._bubble_body(frm_name) == '%s\n%s' % (msg2, msg3):
                    return
            except ldtp.LdtpExecutionError:
                screeny = ldtputils.imagecapture()
                raise AssertionError(
                        'notification for second message does not exist',
                        screeny)
            sleep(1)

        raise AssertionError, 'second message was not appended'

    def testRecieveMessageSimple(self, msg1='', msg2='', timeout=5):
        if not self.buddy:
            self.buddy_login()
            sleep(1)

        jid = self.get_account_name('XMPP')

        alias = self.get_account_alias('OtherXMPP')

        #https://bugs.launchpad.net/ubuntu/+source/pidgin-libnotify/+bug/362248
        ldtp.waittillguinotexist(self._bubble_name_from_alias(alias))

        self.buddy.send_message(jid, '', msg1)
        sleep(2)
        self.buddy.send_message(jid, '', msg2)

        result = 1
        count = 0
        frm_name = ''

        while result:
            frm_name = self._bubble_name_from_alias(alias)
            if count != 0:
                frm_name += str(count)
            result = ldtp.waittillguiexist(frm_name)
            if result:
                if self._is_bubble(frm_name) and \
                        self._bubble_body(frm_name) == msg2:
                    break
            count += 1

        if not result:
            raise AssertionError, \
                'did not recieve a message notification bubble.'
