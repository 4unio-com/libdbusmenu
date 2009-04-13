from desktoptesting.gnome import Application
from shutil import move, rmtree, copytree
import ldtp, ooldtp
import os, traceback
from time import time, sleep
from ConfigParser import ConfigParser
from string import Formatter

class Pidgin(Application):
    WINDOW = "frmBuddyList"
    LAUNCHER = "pidgin"

    TTBL_BUDDIES = "ttbl0"

    DLG_ACCOUNTS = "dlgAccounts"
    DLG_ADD_ACCOUNT = "dlgAddAccount"
    BTN_ADD = "btnAdd"
    CBO_PROTOCOL = "cboProtocol"
    TBL_ACCOUNTS = "tbl0"

    def emptyTest(self):
        print 'empty test'

    def setup(self):
        self.open()

    def teardown(self):
        self.exit()

    def cleanup(self):
        #TODO: it should delete all the "My Personal Keys"
        self.exit()
        self.open()

    def open(self, clean_profile=True, 
             profile_template='./data/purple',
             credentials='./data/credentials.ini'):
        self.creds_fn = self.normalize_path(credentials)
        self.credentials = ConfigParser()
        self.credentials.read(self.creds_fn)

        if clean_profile:
            self.backup_config()
            if profile_template:
                self.generate_profile(self.normalize_path(profile_template))

        Application.open_and_check_app(self)

    def generate_profile(self, profile_template):
        os.mkdir(os.path.expanduser('~/.purple'))
        flat_dict = {}
        if self.credentials:
            for s in self.credentials.sections():
                for k, v in self.credentials.items(s):
                    flat_dict[s+'_'+k] = v

        formatter = Formatter()
        for fn in os.listdir(profile_template):
            if os.path.isdir(os.path.join(profile_template, fn)):
                copytree(os.path.join(profile_template, fn),
                         os.path.join(os.path.expanduser('~/.purple'), fn))
                continue
            buf = open(os.path.join(profile_template, fn)).read()
            f = open(os.path.join(os.path.expanduser('~/.purple'), fn), 'w')
            try:
                buf = formatter.format(buf, **flat_dict)
            except KeyError, e:
                raise Exception, \
                    'no section/key in %s: %s' % (self.creds_fn, e)
            f.write(buf)
            f.close()

    def normalize_path(self, path):
        return os.path.normpath(
            os.path.join(os.path.dirname(__file__), path))

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
        else:
            self.backup_path = backup_path

    def restore_config(self):
        try:
            rmtree('~/.purple')
        except OSError:
            pass

        try:
            move(self.backup_path,
                 os.path.expanduser('~/.purple'))
        except IOError:
            traceback.print_exc()

    def wait_for_account_connect(self, account_name, protocol, timeout=15):
        starttime = time()
        while not self.account_connected(account_name, protocol):
            if time() - starttime >= timeout:
                raise Exception('IM server connection timed out')
            sleep(1)

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
                # TODO, put in resource and protocol for more accuracy.
                if parent.startswith('mnu%s' % account_name) and \
                        parent.endswith('(%s)' % protocol):
                    return False
        return True

    def buddy_available(self, alias):
        return ldtp.doesrowexist(self.WINDOW, self.TTBL_BUDDIES, alias)

    def wait_for_buddy(self, alias, timeout=15):
        starttime = time()
        while not self.buddy_available(alias):
            if time() - starttime >= timeout:
                raise Exception('waiting for buddy timed out')
            sleep(1)

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
        if hasattr(self, 'backup_path'):
            self.restore_config()
        Application.exit(self)
        
