from desktoptesting.test_suite.pidgin import PidginTestSuite
from ConfigParser import ConfigParser
import ldtp, ooldtp, ldtputils
from time import sleep

class PidginNewAccountTest(PidginTestSuite):
    def testNewAccount(self, protocol=None):
        cp = self.application.credentials

        if not cp.has_section(protocol):
            raise Exception(
                'no %s protocol configured in %s' % (protocol, 
                                                     self.application.creds_fn))

        ldtp.waittillguiexist(self.application.DLG_ACCOUNTS, 
                              self.application.BTN_ADD)

        dlg_accounts = ooldtp.context(self.application.DLG_ACCOUNTS)

        btn_add = dlg_accounts.getchild(self.application.BTN_ADD)

        btn_add.click()

        ldtp.waittillguiexist(self.application.DLG_ADD_ACCOUNT)

        dlg_add_account = ooldtp.context(self.application.DLG_ADD_ACCOUNT)

        cbo_protocol = dlg_add_account.getchild(self.application.CBO_PROTOCOL)

        cbo_protocol.comboselect(protocol)

        sleep(1)

        ldtp.remap(self.application.DLG_ADD_ACCOUNT)

        details = dict(cp.items(protocol))

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

        username = self.application.get_account_name(protocol, True)

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
        if  cellval != protocol:
            fails.append(
                'wrong protocol in accounts view (expected %s, got %s)' % \
                    (protocol, cellval))

        if fails:
            raise AssertionError(','.join(fails)+'.', ldtputils.imagecapture())

        # TODO: Should we test successful connection too?
