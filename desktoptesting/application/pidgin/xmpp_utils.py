#!/usr/bin/python -u

import gobject, gtk
import sys
from time import sleep
import traceback

from pyxmpp.all import JID,Iq,Presence,Message,StreamError
from pyxmpp.jabber.client import JabberClient
from pyxmpp.jabber.clientstream import LegacyAuthenticationError

from pyxmpp.jabber.simple import xmpp_do
from pyxmpp.jabber.register import Register

class ClientXMPP(JabberClient):
    def __init__(self, jid, password, debug=False):
        if isinstance(jid, str) or isinstance(jid, unicode):
            jid = JID(jid)

        self.main_loop = gobject.MainLoop()
        self.is_connected = False
        self.messages = []
        self._exception = None
        self.debug = debug

        self.name = jid.node
        self.email = jid.as_unicode()

        # if bare JID is provided add a resource -- it is required
        if not jid.resource:
            jid=JID(jid.node, jid.domain, "UDT")

        # setup client with provided connection information
        # and identity data
        JabberClient.__init__(self, jid, password,
                disco_name="PyXMPP example: echo bot", disco_type="bot")

    def connected(self):
        self.is_connected = True
        JabberClient.connected(self)

    def disconnected(self):
        self.is_connected = False
        JabberClient.disconnected(self)

    def process_registration_form(self, stanza, form):
        if not 'FORM_TYPE' in form or \
                'jabber:iq:register' not in form['FORM_TYPE'].values:
            raise RuntimeError, "Unknown form type: %r %r" % (form, form['FORM_TYPE'])
        for field in form:
            if field.name == u"username":
                field.value = self.jid.node
            elif field.name == u"password":
                field.value = self.password
            elif field.name == u"name":
                field.value = self.name
            elif field.name == u"email":
                field.value = self.email
            elif field.required:
                raise RuntimeError, "Unsupported required registration form field %r" % (field.name,)
        self.submit_registration_form(form)


    def stream_state_changed(self,state,arg):
        if self.debug:
            print "- %s %r" % (state,arg)

    def session_started(self):
        JabberClient.session_started(self)

        # set up handler for <message stanza>
        self.stream.set_message_handler("normal",self.message)

    def message(self,stanza):
        if stanza.get_type() == "chat":
            self.messages.append((stanza.get_from().as_unicode(), 
                                  stanza.get_subject(), 
                                  stanza.get_body()))

    def loop_iter(self, timeout=1):
        if self.stream:
            try:
                self.stream.loop_iter(timeout)
            except Exception, e:
                self._exception = sys.exc_info()
                self.main_loop.quit()
        return True

    def loop(self):
        self.main_loop.run()
        if self._exception:
            exceptionType, exceptionValue, exceptionTraceback = self._exception
            #traceback.print_exception(exceptionType, exceptionValue, 
            #                          exceptionTraceback, file=sys.stdout)
            e = exceptionValue
            self._exception = None
            raise e

    def match_messages(self, jid, subject, body):
        matched = []
        for mjid, msubject, mbody in self.messages:
            if jid is not None and jid != mjid:
                continue
            if subject is not None and subject != msubject:
                continue
            if body is not None and body != mbody:
                continue
            matched.append((mjid, msubject, mbody))

        return matched

    def flush_messages(self):
        while True:
            try:
                self.messages.pop(0)
            except IndexError:
                break
        
def unregister(jid, passwd):
    if not jid.resource:
        jid=JID(jid.node, jid.domain, "remover")
        
    def _remove(stream):
        iq = Iq(from_jid=jid, to_jid=jid.domain, stanza_type="set")
        r = Register()
        r.remove = True
        iq.set_content(r)
        stream.send(iq)

    xmpp_do(jid, passwd, _remove)

def register(jid, passwd):
    b = Buddy(JID(jid), passwd)
    try:
        b.connect(True)
    except LegacyAuthenticationError:
        pass
    finally:
        b.disconnect()

if __name__ == "__main__":
    b = Buddy(JID(sys.argv[1]), sys.argv[2])
    b.connect()
    print 'connected?'
    #b.client.loop()
    while True:
        msg = b.wait_for_message(timeout=1)
        if msg:
            print msg

    #sleep(1)
    #print b.wait_for_message(timeout=5)
    #b.disconnect()
