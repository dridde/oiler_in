#!/usr/bin/env python
# -*- coding:utf-8 -*-

import config

from oilib.helpers import *
from oilib.connection import IRCConnection

def handle_privmsg(irc, nick, userhost, target, message):
	print '<%s@%s/%s> %s' % (nick, userhost, target, message)
	return True

def handle_kick(irc, nick, userhost, target, victim):
	irc.send('JOIN', target)
	return True

def handle_unknown(irc, prefix, command, args):
	print 'UNKOWN: %s %s %s' % (prefix, command, args)
	return False

def main():
	irc = IRCConnection(server=config.server, port=config.port, password=config.password, nick=config.nick, realname=config.realname, user=config.user, channels=[config.chan])
	irc.on('privmsg', handle_privmsg)
	irc.on('kick', handle_kick)
	irc.on('*', handle_unknown)
	irc.connect()

if __name__ == "__main__":
	main()
