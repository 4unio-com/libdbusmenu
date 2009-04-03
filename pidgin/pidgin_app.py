from desktoptesting.gnome import Application
from shutil import move, rmtree
import ldtp, ooldtp
import os, traceback
from time import time, sleep

class Pidgin(Application):
    WINDOW = "frmBuddyList"
    LAUNCHER = "pidgin"

    TTBL_BUDDIES = "ttbl0"

    DLG_ACCOUNTS = "dlgAccounts"
    DLG_ADD_ACCOUNT = "dlgAddAccount"
    BTN_ADD = "btnAdd"
    CBO_PROTOCOL = "cboProtocol"
    TBL_ACCOUNTS = "tbl0"

    def setup(self):
        self.open()

    def teardown(self):
        self.exit()

    def cleanup(self):
        #TODO: it should delete all the "My Personal Keys"
        self.exit()
        self.open()

    def open(self, clean_profile=True):
        self.backup_config()
        Application.open_and_check_app(self)

    def backup_config(self):
        p = os.path.expanduser('~/.purple.bak')
        backup_path = p
        i = 2
        while os.path.exists(backup_path):
            backup_path = '%s.%d' % (p, i)
            i += 1

        try:
            move(os.path.expanduser('~/.purple'), backup_path)
        except IOError:
            pass

    def restore_config(self):
        try:
            rmtree('~/.purple')
        except OSError:
            traceback.print_exc()
            pass

        try:
            move(os.path.expanduser('~/.purple.bak'), 
                 os.path.expanduser('~/.purple'))
        except IOError:
            traceback.print_exc()
            pass

    def wait_for_account_connect(self, account_name, protocol, timeout=5):
        starttime = time()
        while not self.account_connected(protocol, protocol):
            sleep(1)
            if time() - starttime >= connect_timeout:
                raise Exception('IM server connection timed out')

    def account_connected(self, account_name, protocol):
        '''Checks to see if a specified account is connected, it parsed the 
        account's submenu, if there is a menu item "no actions available", then
        the account is not yet connected.
        '''
        ldtp.remap(self.WINDOW)
        window = ooldtp.context(self.WINDOW)
        objs = window.getobjectlist()
        for obj in objs:
            if obj.startswith('mnuNoactionsavailable'):
                parent = ldtp.getobjectproperty(self.WINDOW,obj, 'parent')
                print parent, parent.startswith('mnu%s' % account_name), \
                    parent.endswith('(%s)' % protocol), account_name, protocol
                # TODO, put in resource and protocol for more accuracy.
                if parent.startswith('mnu%s' % account_name) and \
                        parent.endswith('(%s)' % protocol):
                    return False
        return True

    def send_message(self, alias, msg):
        if not ldtp.doesrowexist(self.WINDOW, self.TTBL_BUDDIES, alias):
            raise Exception("user %s is not online" % alias)
        ldtp.selectrow(self.WINDOW, self.TTBL_BUDDIES, alias)
        ldtp.generatekeyevent('<return>')

        ldtp.waittillguiexist('frm' + alias.replace(' ', ''))

        frame = ooldtp.context('frm' + alias.replace(' ', ''))

        frame.settextvalue('txt1', msg)

        ldtp.generatekeyevent('<return>')

    def exit(self):
        Application.exit(self)
        
