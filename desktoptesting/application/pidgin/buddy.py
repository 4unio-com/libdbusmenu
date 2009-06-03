#!/usr/bin/python -u

import gobject, gtk

from xmpp_utils import ClientXMPP
from msn_utils import ClientMSN

class _Buddy(object):
    """
    The Buddy class is a class to mimic a Buddy behaviour in IM
    applications. It is intended to be use as "VirtualBuddy" in any
    test for IMs. It could be used in tests for Pidgin, Empathy, etc.

    Buddy is an interface for the different IMs protocol
    """
    def __init__(self, userid, passwd, protocol):
        """
        To init the buddy class, use the new_buddy method instead
        """
        pass

    def connect(self, register=False, name='', email=''):
        """
        It connects the buddy to the specific protocol server.

        @type register: boolean
        @param register: True, to register the name and the email
            of the buddy. False, otherwise. It defaults to false.
        @type name: string
        @param name: The name of the buddy to register
        @type email: string
        @param email: The email of the buddy to register
        """
        raise NotImplementedError
        
    def disconnect(self):
        """
        It disconnects the buddy from the specific protocol server.
        """
        raise NotImplementedError

    def send_message(self, userid, body='', subject=''):
        """
        It sends a message to a specific user.

        @type userid: string
        @param userid: The userid of the recipient of the message.
        @type body: string
        @param body: The contents of the message, if any.
        @type subject: string
        @param subject: The subject of the message, if any.
        """
        raise NotImplementedError

    def wait_for_message(self, userid=None, body=None, subject=None, timeout=5):
        """
        It waits for a message of a specific user.

        @type userid: string
        @param userid: The user account from whom we are wating the message.
        @type body: string
        @param body: The contents of the message, if specified.
        @type subject: string
        @param subject: The subject of the message, if specified.
        @type timeout: integer
        @param timeout: Number of seconds to wait for the message.
        """
        raise NotImplementedError


class _BuddyXMPP(_Buddy):
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
        
    def send_message(self, userid, body, subject=''):
        self.client.send_message(userid, body, subject)

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

class _BuddyMSN(_Buddy):
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
                client.send_text_message_to_current_conversation(body)
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


    def wait_for_message(self, userid=None, body=None, subject=None, timeout=5):
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


buddy_protocols = {'XMPP' : _BuddyXMPP,
                   'MSN' : _BuddyMSN}

def new_buddy(userid, passwd, protocol):
    """
    Factory method to create a new buddy instance.

    @type userid: string
    @param userid: The user id of the new buddy.
    @type passwd: string
    @param passwd: The password of the new buddy.
    @type protocol: string 
    @param protocol: The IM protocol to use
    """
    return buddy_protocols[protocol](userid, passwd)
