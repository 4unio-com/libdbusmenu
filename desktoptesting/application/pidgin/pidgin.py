from ..main import Application
from shutil import move, rmtree, copytree
import ldtp, ooldtp
import os, traceback
from time import time, sleep
from ConfigParser import ConfigParser
from string import Formatter
from buddy import new_buddy
from inspect import getsourcefile

class AccountInfo(object):
    PURPLE_PROTOCOLS = {
        'XMPP' : 'prpl-jabber'
        }
    def __init__(self, name, credentials):
        if not isinstance(credentials, ConfigParser):
            creds_fn = credentials
            credentials = ConfigParser()
            credentials.read(creds_fn)
        self.details = dict(credentials.items(name))
        self.name = name

    def __getattr__(self, name):
        try:
            return self.details[name]
        except KeyError:
            raise AttributeError

    @property
    def prpl_protocol(self):
        return self.PURPLE_PROTOCOLS[self.protocol]

    @property
    def username(self):
        return self._get_username(False)

    @property
    def alias(self):
        return self.details.get('alias', self._get_username(False))

    @property
    def username_and_domain(self):
        return self._get_username(True)

    @property
    def template_args(self):
        args = {}
        for arg in ('prpl_protocol', 'username_and_domain', 
                    'password', 'alias'):
            args[arg] = getattr(self, arg)
        return args

    def _get_username(self, include_resource=False):
        if self.protocol == 'XMPP':
            username = '%s@%s' % (self.details['username'],
                                  self.details['domain'])
            if include_resource:
                username += '/%s' % self.details['resource']
        else:
            username = self.details['username']
        return username

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

    def open(self, clean_profile=True, credentials=''):
        """
        It saves the old profile (if needed) and
        set up a new one. After this initial process,
        it opens the application

        @type clean_profile: boolean
        @param clean_profile: True, to back up the old profile and create a 
            new one (default)
        @type credentials: string
        @param credentials: Path to the config file with accounts information
        """
        clean_profile = clean_profile not in ('False', '0', False)
        self.creds_fn = self._normalize_path(credentials)
        self.credentials = ConfigParser()
        self.credentials.read(self.creds_fn)
        self.buddy = None

        if clean_profile:
            self.backup_config()

        Application.open(self)

    def generate_profile(self, profile_template, template_args=None):
        """
        It uses the profile_template and the
        credentials to build a new profile folder
        """
        os.mkdir(os.path.expanduser('~/.purple'))

        formatter = Formatter()
        for fn in os.listdir(profile_template):
            if os.path.isdir(os.path.join(profile_template, fn)):
                copytree(os.path.join(profile_template, fn),
                         os.path.join(os.path.expanduser('~/.purple'), fn))
                continue
            buf = open(os.path.join(profile_template, fn)).read()
            f = open(os.path.join(os.path.expanduser('~/.purple'), fn), 'w')
            try:
                buf = formatter.format(buf, **template_args)
            except KeyError, e:
                raise Exception, \
                    'no section/key in %s: %s' % (self.creds_fn, e)
            f.write(buf)
            f.close()

    def _normalize_path(cls, path):
        return path
#        return os.path.normpath(
#            os.path.join(os.path.dirname(getsourcefile(cls)), path))
    _normalize_path = classmethod(_normalize_path)

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

    def wait_for_account_connect(self, account_info, timeout=15):
        """
        It waits for an account to be connected.
        A timeout value can be passed, being default 15secs.

        It raises an exception if the timeout expires.

        @param account_info: The account information.
        @type account_info: L{AccountInfo}
        @param timeout: Number of seconds to wait for the accout to be connected (default:15s)
        @type timeout: integer
        """
        starttime = time()
        print 'wait_for_account_connect'
        while not self.account_connected(account_info):
            if time() - starttime >= timeout:
                raise Exception('IM server connection timed out')
            exists = ldtp.waittillguiexist('dlgSSLCertificateVerification',
                                           guiTimeOut=1)
            print exists, time() - starttime
            if exists:
                ldtp.click('dlgSSLCertificateVerification', 'btnAccept')

    def account_connected(self, account_info):
        '''
        Checks to see if a specified account is connected,
        @param account_info: The account information.
        @type account_info: L{AccountInfo}

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
                print 'mnu%s' % account_info.username_and_domain
                if parent.startswith(
                    'mnu%s' % account_info.username_and_domain) and \
                    parent.endswith('(%s)' % account_info.protocol):
                    print 'False?'
                    return False
        print 'True?'
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

    def close(self):
        """
        It restore the previous configuration of Pidgin and exists
        """
        if hasattr(self, 'backup_path'):
            self.restore_config()
        Application.close(self)
        
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

    def buddy_login(self, account_info):
        self.buddy = \
            new_buddy(account_info.username,
                      account_info.password,
                      account_info.protocol)

        print 'connecting buddy'
        self.buddy.connect()
        print 'connected buddy'

