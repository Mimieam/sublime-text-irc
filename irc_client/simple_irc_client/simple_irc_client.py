# IRCClient
#
import functools

import sublime

from IRC.utils import get_setting
from IRC.irc_client.irc_gntp_client import IrcGntpClient

from .irc import client


# T H R E A D S
# =============
#
# A number of things need to happen on the main thread so create a helper
# function:
#
def main_thread(callback, *args, **kwargs):

    sublime.set_timeout(functools.partial(callback, *args, **kwargs), 0)


def parse_nickname(nickname):

    return nickname.split('!')

    
class IRCClient(client.SimpleIRCClient):

    def __init__(self, writer, target, nickname, on_disconnect=None, quit_message='Using sublime IRC.'):

        # Initialise the base class:
        #
        client.SimpleIRCClient.__init__(self)

        self.nickname = nickname
        self.on_disconnect_callback = on_disconnect
        self.quit_message = quit_message
        self.target = target
        self.writer = writer
        self.growl = IrcGntpClient(self)
      
    def on_welcome(self, connection, event):

        self.writer(' '.join(event.arguments))
        if client.is_channel(self.target):
            connection.join(self.target)

    def on_privmsg(self, connection, event):

        who, host = parse_nickname(event.source)
        self.writer(u'PRIVMSG: {0} ({1}): {2}'.format(who, host, ' '.join(event.arguments)))

    def on_privnotice(self, connection, event):

        self.writer(u'Private Notice: {0}: {1}'.format(event.source, ' '.join(event.arguments)))

    def on_pubmsg(self, connection, event):

        def for_threading():
            who, host = parse_nickname(event.source)
            if get_setting('show_host_in_messages', False):
                self.writer(u'{0} ({1}): {2}'.format(who, host, ' '.join(event.arguments)))
            else:
                self.writer(u'{0}: {1}'.format(who, ' '.join(event.arguments)))
                print (u'{0} ({1}vs{2}) : {3}'.format(self.nickname in event.arguments[0], self.nickname,self.connection.get_nickname() ,' '.join(event.arguments)))
                if self.connection.get_nickname() in event.arguments[0]:
                    print ('about to notify')
                    if get_setting('show_prvmsg_in_growl'):
                        self.growl.quickNotify(u'{0}: {1}'.format(who, ' '.join(event.arguments)))

        main_thread(
            for_threading
        )

    def on_pubnotice(self, connection, event):

        self.writer(u'Public Notice: {0}: {1}'.format(event.source, ' '.join(event.arguments)))

    def on_disconnect(self, connection, event):

        self.writer(u'*** Disconnected from {0}'.format(event.source))
        if self.on_disconnect_callback is not None:
            self.on_disconnect_callback()

    def on_error(self, connection, event):

        self.writer(u'*** Error {0}'.format(' '.join(event.arguments)))

    def on_join(self, connection, event):

        who, host = parse_nickname(event.source)
        if who == self.get_nickname():
            who_joined = u'You have'
        else:
            who_joined = u'{0} ({1}) has'.format(who, host)
        self.writer(u'*** {0} joined channel {1}'.format(who_joined, event.target))


    def on_motd(self, connection, event):

        self.writer(u'*** MOTD {0}'.format(' '.join(event.arguments)))

    def on_namreply(self, connection, event):

        self.writer(u'*** NAMRPLY {0}'.format(' '.join(event.arguments)))

    def on_ping(self, connection, event):

        if get_setting('show_ping_messages', False):
            self.writer(u'*** PING {0}'.format(' '.join(event.arguments)))

    def on_all_raw_messages(self, connection, event):

        if get_setting('show_all_raw_messages', False):
            self.writer(u'*** ARM {0}'.format(' '.join(event.arguments)))

    def on_nicknameinuse(self, connection, event):

        # We could try again with a different nickname, for example,
        # with a number or underscore appended:
        #
        self.writer(u'*** Nickname \'{0}\' is already in use on server {1}'.format(self.nickname, event.source))

    def write(self, msg):
        if get_setting('show_prvmsg_in_growl'):
            self.growl.quickNotify('new test growl',msg)
        self.connection.privmsg(self.target, msg)

    def get_nickname(self):

        return self.connection.get_nickname()

    # Commands:
    #
    def command(self, command):

        conn = self.connection

        tokens = command.split()
        command = tokens[0].lower()

        # The /nick command either returns the current nickname or sets
        # a new one:
        #
        if command == '/nick':
            if len(tokens) != 2:
                self.writer(conn.get_nickname())
            else:
                conn.nick(tokens[1])
                print(conn.get_nickname() != self.nickname , self.nickname)
                if conn.get_nickname() != self.nickname:  #we need to change the internal name also
                    self.nickname = conn.get_nickname()
        # The /quit and /connect commands do what they say on the tin:
        #
        if command == '/quit':
            conn.quit(self.quit_message)

        if command == '/connect':
            conn.reconnect()
