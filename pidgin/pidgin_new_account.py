from pidgin_app import Pidgin
from ConfigParser import ConfigParser
import ldtp, ooldtp, ldtputils
from time import sleep

class PidginNewAccountTest(Pidgin):
    DLG_ACCOUNTS = "dlgAccounts"
    DLG_ADD_ACCOUNT = "dlgAddAccount"
    BTN_ADD = "btnAdd"
    CBO_PROTOCOL = "cboProtocol"
    TBL_ACCOUNTS = "tbl0"
    def testNewAccount(self, credentials=None, protocol=None):
        cp = ConfigParser()
        cp.read(credentials)

        if not cp.has_section(protocol):
            raise Exception(
                'no %s protocol configured in %s' % (protocol, credentials))

        dlg_accounts = ooldtp.context(self.DLG_ACCOUNTS)

        btn_add = dlg_accounts.getchild(self.BTN_ADD)

        btn_add.click()

        ldtp.waittillguiexist(self.DLG_ADD_ACCOUNT)

        dlg_add_account = ooldtp.context(self.DLG_ADD_ACCOUNT)

        cbo_protocol = dlg_add_account.getchild(self.CBO_PROTOCOL)

        cbo_protocol.comboselect(protocol)

        sleep(1)

        ldtp.remap(self.DLG_ADD_ACCOUNT)

        details = dict(cp.items(protocol))

        for name, value in details.items():
            dlg_add_account.settextvalue('txt%s' % name.capitalize(), value)

        btn_add = dlg_add_account.getchild(self.BTN_ADD)

        btn_add.click()

        sleep(1)

        last_row = dlg_accounts.getrowcount(self.TBL_ACCOUNTS) - 1

        print 'last_row', last_row

        if last_row < 0:
            raise AssertionError("no new accounts in view.", 
                                 ldtputils.imagecapture())

        if protocol == "XMPP":
            username = '%s@%s/%s' % (details['username'], 
                                     details['domain'],
                                     details.get('resource', ''))
        else:
            username = details['username']

        try:
            dlg_accounts.getcellvalue(self.TBL_ACCOUNTS, 0, 1)
        except:
            # Don't know why but first getcellvalue() always fails..
            pass
        
        fails = []

        cellval = dlg_accounts.getcellvalue(self.TBL_ACCOUNTS, 0, 1)
        if cellval != username:
            fails.append(
                'wrong username in accounts view (expected %s, got %s)' % \
                    (username, cellval))

        cellval = dlg_accounts.getcellvalue(self.TBL_ACCOUNTS, 0, 2)
        if  cellval != protocol:
            fails.append(
                'wrong protocol in accounts view (expected %s, got %s)' % \
                    (protocol, cellval))

        if fails:
            raise AssertionError(','.join(fails)+'.', ldtputils.imagecapture())

        # TODO: Should we test successful connection too?
