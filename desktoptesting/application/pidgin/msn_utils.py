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
            print "Connected"

    def on_client_error(self, error_type, error):
        print "ERROR :", error_type, " ->", error

class InviteEvents(pymsn.event.InviteEventInterface):
    def __init__(self, client):
        self.conv = ''
    def on_invite_conversation(self, conversation):
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
        if self.body != '':
            self._client.send_text_message(pymsn.ConversationMessage(self.body))
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

class ClientMSN(pymsn.Client):
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

    def send_text_message_to_current_conversation(self, body):
        self.conv.send_text_message(pymsn.ConversationMessage(body))

    def loop_iter(self):
        pass

    def loop(self):
        self.main_loop.run()

    def connection_stablished(self):
        if self.state == pymsn.event.ClientState.OPEN:
            return True
        else:
            return False


