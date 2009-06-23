from mago.test_suite.pidgin import PidginTestSuite
from mago.application.pidgin import AccountInfo
from ConfigParser import ConfigParser
import ldtp, ooldtp, ldtputils
from time import sleep

class PidginNewAccountTest(PidginTestSuite):
    def __init__(self, credentials):
        PidginTestSuite.__init__(
            self, clean_profile=True, credentials=credentials)

    def testNewAccount(self, account_name=None):

        if not self.application.credentials.has_section(account_name):
            raise Exception(
                'no %s account configured in %s' % (account_name, 
                                                    self.application.creds_fn))

        account_info = AccountInfo(account_name, self.application.credentials)

        ldtp.waittillguiexist(self.application.DLG_ACCOUNTS, 
                              self.application.BTN_ADD)

        dlg_accounts = ooldtp.context(self.application.DLG_ACCOUNTS)

        btn_add = dlg_accounts.getchild(self.application.BTN_ADD)

        btn_add.click()

        ldtp.waittillguiexist(self.application.DLG_ADD_ACCOUNT)

        dlg_add_account = ooldtp.context(self.application.DLG_ADD_ACCOUNT)

        cbo_protocol = dlg_add_account.getchild(self.application.CBO_PROTOCOL)

        cbo_protocol.comboselect(account_info.protocol)

        sleep(1)

        ldtp.remap(self.application.DLG_ADD_ACCOUNT)

        details = account_info.details

        for name, value in details.items():
            if name not in ('username', 'domain', 'resource', 'password'):
                continue
            dlg_add_account.settextvalue('txt%s' % name.capitalize(), value)

        btn_add = dlg_add_account.getchild(self.application.BTN_ADD)

        btn_add.click()

        sleep(1)

        last_row = dlg_accounts.getrowcount(self.application.TBL_ACCOUNTS) - 1

        print 'last_row', last_row

        if last_row < 0:
            raise AssertionError("no new accounts in view.", 
                                 ldtputils.imagecapture())

        username = account_info.username_and_domain

        try:
            dlg_accounts.getcellvalue(self.application.TBL_ACCOUNTS, 0, 1)
        except:
            # Don't know why but first getcellvalue() always fails..
            pass
        
        fails = []

        cellval = dlg_accounts.getcellvalue(self.application.TBL_ACCOUNTS, 0, 1)
        if cellval != username:
            fails.append(
                'wrong username in accounts view (expected %s, got %s)' % \
                    (username, cellval))

        cellval = dlg_accounts.getcellvalue(self.application.TBL_ACCOUNTS, 0, 2)
        if  cellval != account_info.protocol:
            fails.append(
                'wrong protocol in accounts view (expected %s, got %s)' % \
                    (account_info.protocol, cellval))

        if fails:
            raise AssertionError(','.join(fails)+'.', ldtputils.imagecapture())

        # TODO: Should we test successful connection too?
