from desktoptesting.gnome import Application
from shutil import move, rmtree, copytree
import ldtp, ooldtp
import os, traceback
from time import time, sleep
from ConfigParser import ConfigParser
from string import Formatter

class Pidgin(Application):    
    # Pidgin constants
    WINDOW = "frmBuddyList"
    LAUNCHER = "pidgin"

    TTBL_BUDDIES = "ttbl0"

    DLG_ACCOUNTS = "dlgAccounts"
    DLG_ADD_ACCOUNT = "dlgAddAccount"
    BTN_ADD = "btnAdd"
    CBO_PROTOCOL = "cboProtocol"
    TBL_ACCOUNTS = "tbl0"

    MNU_CLOSE = "mnuClose"
    
    def emptyTest(self):
        print 'empty test'
        ldtp.generatekeyevent('<alt><F9>')
        sleep(3)

    def setup(self):
        self.open()

    def teardown(self):
        self.exit()

    def cleanup(self):
        self.exit()
        self.open()

    def open(self, clean_profile=True, 
             profile_template='./data/purple',
             credentials='./data/credentials.ini'):
        """
        It saves the old profile (if needed) and
        set up a new one. After this initial process,
        it opens the application

        @type clean_profile: boolean
        @param clean_profile: True, to back up the old profile and create a 
            new one (default)
        @type profile_template: string
        @param profile_template: Path to the template of the new profile
        @type credentials: string
        @param credentials: Path to the config file with accounts information
        """
         
        self.creds_fn = self.normalize_path(credentials)
        self.credentials = ConfigParser()
        self.credentials.read(self.creds_fn)

        if clean_profile:
            self.backup_config()
            if profile_template:
                self.generate_profile(self.normalize_path(profile_template))

        Application.open_and_check_app(self)

    def generate_profile(self, profile_template):
        """
        It uses the profile_template and the
        credentials to build a new profile folder
        """
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
        """
        It saves the configuration of Pidgin in a path
        called ~/.purple.bak{.n}
        """
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
        """
        It deletes the configuration folder and restore then
        one backed up (at backup_path)
        """
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
        """
        It waits for an account to be connected.
        A timeout value can be passed, being default 15secs.

        It raises an exception if the timeout expires.

        @type account_name: string 
        @param account: The name of the account (user name)
        @type protocol: string
        @param protocol: The protocol of the account to wait to be connected
        @type timeout: integer
        @param timeout: Number of seconds to wait for the accout to be connected (default:15s)
        """
        starttime = time()
        while not self.account_connected(account_name, protocol):
            if time() - starttime >= timeout:
                raise Exception('IM server connection timed out')
            sleep(1)

    def account_connected(self, account_name, protocol):
        '''
        Checks to see if a specified account is connected,
        @type account_name: string
        @param account_name: The name of the account (user name)
        @type protocol: string
        @param protocol: The name of the protocol used 

        @return True, if the account if connected, False if not.
        '''
        ldtp.remap(self.WINDOW)
        window = ooldtp.context(self.WINDOW)
        objs = window.getobjectlist()
        # It parses the account's submenu, if there is a menu 
        # item "no actions available", then the account is not yet connected.
        for obj in objs:
            if obj.startswith('mnuNoactionsavailable'):
                parent = ldtp.getobjectproperty(self.WINDOW,obj, 'parent')
                # TODO, put in resource and protocol for more accuracy.
                if parent.startswith('mnu%s' % account_name) and \
                        parent.endswith('(%s)' % protocol):
                    return False
        return True

    def buddy_available(self, alias):
        """
        It searches for a given alias to be in the buddy list

        @type alias: string
        @param alias: The name of the buddy to search

        @return 1, if the buddy is available, 0 otherwise.
        """
        return ldtp.doesrowexist(self.WINDOW, self.TTBL_BUDDIES, alias)

    def wait_for_buddy(self, alias, timeout=15):
        """
        It waits for a buddy to be connected.
        A timeout value can be passed, being default 15secs.

        It raises an exception if the timeout expires.

        @type alias: string 
        @param alias: The name of the buddy to wait to be available
        @type timeout: integer
        @param timeout: Number of seconds to wait for the buddy to be connected (default:15s)
        """
        starttime = time()
        while not self.buddy_available(alias):
            if time() - starttime >= timeout:
                raise Exception('waiting for buddy timed out')
            sleep(1)

    def send_message(self, alias, msg):
        """
        It sends a message to a particular buddy.

        It raises an exception if the particuar buddy is not online.

        @type alias: string
        @param alias: The name of the buddy to send the message to
        @type msg: string
        @param msg: The message to send to the buddy
        """
        if not ldtp.doesrowexist(self.WINDOW, self.TTBL_BUDDIES, alias):
            raise Exception("user %s is not online" % alias)
        ldtp.selectrow(self.WINDOW, self.TTBL_BUDDIES, alias)
        ldtp.generatekeyevent('<return>')

        ldtp.waittillguiexist('frm' + alias.replace(' ', ''))
        
        frame = ooldtp.context('frm' + alias.replace(' ', ''))

        frame.settextvalue('txt1', msg)

        ldtp.generatekeyevent('<return>')

    def get_conversation_log(self, alias):
        """
        It gets the text of a on-going conversation (no backlog)

        @type alias: string
        @param alias: The buddy to get the conversation text

        @return The text of the conversion. '' if the conversation does not exist
        """
        if not ldtp.guiexist('frm' + alias.replace(' ', '')):
            return ''

        return ldtp.gettextvalue('frm' + alias.replace(' ', ''), 'txt0')

    def exit(self):
        """
        It restore the previous configuration of Pidgin and exists
        """
        if hasattr(self, 'backup_path'):
            self.restore_config()
        Application.exit(self)
        
    def get_all_windows(self):
        """
        It gets the list of the pidgin windows

        @return A list containing the name of the windows
        """
        windows = []
        print self.name
        for w in ldtp.getwindowlist():
            try:
                if ldtp.getobjectproperty(w, w, 'parent') == 'pidgin':
                    windows.append(w)
            except LdtpExecutionError:
                continue
        return windows
    
    def close_conversation(self, window_name):
        """
        It closes a conversation window

        @type window_name: string
        @param window_name: The name of the conversation to close
        """
        ldtp.selectmenuitem(window_name, self.MNU_CLOSE)
