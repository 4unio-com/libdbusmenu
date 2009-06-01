#!/usr/bin/python -u

import gobject, gtk

from xmpp_utils import ClientXMPP
from msn_utils import ClientMSN

class Buddy(object):
    def __init__(self, userid, passwd, protocol):
        self.protocol = protocol

        if protocol == 'XMPP':
            self.protocolbuddy = _BuddyXMPP(userid, passwd)
        elif protocol == 'MSN':
            self.protocolbuddy = _BuddyMSN(userid, passwd)
        else:
            pass

    def connect(self, register=False, name='', email=''):
        self.protocolbuddy.connect(register, name, email)        
        
    def disconnect(self):
        self.protocolbuddy.disconnect() 

    def send_message(self, userid, body='', subject='') :
        self.protocolbuddy.send_message(userid, body, subject)

    def wait_for_message(self, userid=None, body=None, timeout=5):
        self.protocolbuddy.wait_for_message(userid, body, timeout)


class _BuddyXMPP(object):
    def __init__(self, userid, passwd):
                
        self.account = (userid, passwd)
        self.client = ClientXMPP(userid, passwd)
        
    def connect(self, register=False, name='', email=''):
        def _idle_cb(client):
            client.loop_iter()
            if client.session_established:
                client.main_loop.quit()
                return False
            else:
                return True

        if register and name:
            self.client.name = name
        if register and email:
            self.client.email = email

        self.client.connect(register)
        gobject.idle_add(_idle_cb, self.client)
        self.client.loop()

    def disconnect(self):
        def _idle_cb(client):
            client.loop_iter()
            if not client.is_connected:
                client.main_loop.quit()
                return False
            else:
                return True

        self.client.disconnect()
        gobject.idle_add(_idle_cb, self.client)
        self.client.loop()
        
    def send_message(self, userid, subject, body):
        m=Message(
            to_jid=unicode(userid),
            from_jid=self.client.jid.as_unicode(),
            stanza_type="chat",
            subject=unicode(subject),
            body=unicode(body))
        self.client.stream.send(m)

    def wait_for_message(self, userid=None, subject=None, body=None, timeout=5):
        pattern = [userid, subject, body]
        recieved = []

        def _idle_cb(client):
            client.loop_iter()
            matched = client.match_messages(*pattern)
            client.flush_messages()
            if matched:
                for m in matched:
                    recieved.append(m)
                client.main_loop.quit()
                return False
            else:
                return True

        def _timeout_cb(client):
            client.main_loop.quit()
            return False

        gobject.idle_add(_idle_cb, self.client)
        if timeout > 0:
            gobject.timeout_add_seconds(timeout, _timeout_cb, self.client)
        self.client.loop()

        return recieved

class _BuddyMSN(object):
    def __init__(self, userid, passwd):
        self.account = (userid, passwd)
        self.client  = ClientMSN(self.account)

    def connect(self, register=False, name='', email=''):
        def _idle_cb(client):
            client.loop_iter()
            if client.connection_stablished():
                client.main_loop.quit()
                return False
            else:
                return True

        if register and name:
            self.client.name = name
        if register and email:
            self.client.email = email

        self.client.connect(register)
        gobject.idle_add(_idle_cb, self.client)
        self.client.loop()

    def disconnect(self):
        def _idle_cb(client):
            client.loop_iter()
            if not client.is_connected:
                client.main_loop.quit()
                return False
            else:
                return True

        self.client.disconnect()
        gobject.idle_add(_idle_cb, self.client)
        self.client.loop()

    def send_message(self, userid, body, subject='') :
        def _idle_cb(client, userid, body):
            client.loop_iter()
            if client.current == userid:
                client.conv.send_text_message(pymsn.ConversationMessage(body))
            else:
                client.start_conversation(userid, body)

        def _wait_for_conversation(client):
            client.loop_iter()
            if client.is_talking:
                if client._convo_events.talking == False:
                    client.is_talking = False
                return True
            else:
                client.main_loop.quit()
                return False

        self.client.is_talking = True
        gobject.idle_add(_idle_cb, self.client, userid, body)
        gobject.idle_add(_wait_for_conversation, self.client)
        self.client.loop()


    def wait_for_message(self, userid=None, body=None, timeout=5):
        recieved = "" 

        def _idle_cb(client):
            client.loop_iter()
            if client._invite_events.conv != '':
                client.conv = client._invite_events.conv
                client._convo_events =  AnnoyingConversation(client.conv, '')

            if client._convo_events is not None:
                if client._convo_events.last_message == body and client.current == userid:
                    recieved = body
                    client.main_loop.quit()
                    return False
                else:
                    return True
            else:
                return True

        def _timeout_cb(client):
            client.main_loop.quit()
            return False

        gobject.idle_add(_idle_cb, self.client)
        if timeout > 0:
            gobject.timeout_add_seconds(timeout, _timeout_cb, self.client)
        self.client.loop()

        return recieved

