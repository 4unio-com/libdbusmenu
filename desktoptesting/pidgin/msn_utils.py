#!/usr/bin/python -u

import gobject, gtk
import sys
from time import sleep
import traceback
import gobject
import pymsn
import pymsn.event

def get_proxies():
    import urllib
    proxies = urllib.getproxies()
    result = {}
    if 'https' not in proxies and \
            'http' in proxies:
        url = proxies['http'].replace("http://", "https://")
        result['https'] = pymsn.Proxy(url)
    for type, url in proxies.items():
        if type == 'no': continue
        if type == 'https' and url.startswith('http://'):
            url = url.replace('http://', 'https://', 1)
        result[type] = pymsn.Proxy(url)
    return result

class ClientEvents(pymsn.event.ClientEventInterface):
    def on_client_state_changed(self, state):
        if state == pymsn.event.ClientState.CLOSED:
            self._client.quit()
        elif state == pymsn.event.ClientState.OPEN:
            self._client.profile.presence = pymsn.Presence.ONLINE
            for contact in self._client.address_book.contacts:
                print contact
            print "Connected"

    def on_client_error(self, error_type, error):
        print "ERROR :", error_type, " ->", error

class InviteEvents(pymsn.event.InviteEventInterface):
    def __init__(self, client):
        self.conv = ''
    def on_invite_conversation(self, conversation):
        print "being invited"
        self.conv = conversation

class AnnoyingConversation(pymsn.event.ConversationEventInterface):
    
    def __init__(self, conv, body):
        pymsn.event.ConversationEventInterface.__init__(self, conv)
        self.talking = True
        self.body    = body
        self.last_message = ""
        self.last_sender = ""

    def on_conversation_user_joined(self, contact):
        gobject.timeout_add(5000, self.annoy_user)

    def annoy_user(self):
        formatting = pymsn.TextFormat("Comic Sans MS", 
                         pymsn.TextFormat.UNDERLINE | pymsn.TextFormat.BOLD,
                         'FF0000')
        if self.body != '':
            self._client.send_text_message(pymsn.ConversationMessage(self.body, formatting))
        self.talking = False
        return False 

    def on_conversation_user_typing(self, contact):
        print "typing"
        pass

    def on_conversation_message_received(self, sender, message):
        self.last_message = message.content
        self.last_sender  = sender.account
        pass

    def on_conversation_error(self, error_type, error):
        print "ERROR :", error_type, " ->", error 	

class _Client(pymsn.Client):
    def __init__(self, account, debug=False):
        server = ('messenger.hotmail.com', 1863)
        
        self.main_loop = gobject.MainLoop()
        self.is_connected = False
        self.messages = []
        self._exception = None
        self.debug = debug
        self.quit = quit
        self.account = account
        self.is_talking = False
        self.current = ''
        self.conv = ''
        self._convo_events = None

        pymsn.Client.__init__(self, server, proxies = get_proxies())
        self._event_handler = ClientEvents(self)
        self._invite_events = InviteEvents(self)

    def connect(self, register):
        self.is_connected = True
        self.login(*self.account)
        return False

    def disconnect(self):
        self.is_connected = False
        self.logout()

    def start_conversation(self, userid, body):
        self.is_talking = True
        contacts = self.address_book.contacts.\
                search_by_presence(pymsn.Presence.ONLINE)

        if len(contacts) == 0:
            print "No online contacts"
            return True
        else:
            for contact in contacts:
                if contact.account == userid:
                    print "Inviting %s for a conversation" % contact.display_name
                    self.conv = pymsn.Conversation(self, [contact])
                    self.current = contact.account
                    self._convo_events = AnnoyingConversation(self.conv, body)
                    self._convo_events.talking = True
            return False

    def loop_iter(self):
        pass

    def loop(self):
        self.main_loop.run()

    def connection_stablished(self):
        if self.state == pymsn.event.ClientState.OPEN:
            return True
        else:
            return False

class BuddyMSN(object):
    def __init__(self, userid, passwd):
        account = (userid, passwd)
        self.client = _Client(account)

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

