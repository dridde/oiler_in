#!/usr/bin/env python
# -*- coding:utf-8 -*-

import config

from oilib.helpers import *
from oilib.connection import IRCConnection

def twitter(irc, nick, userhost, target, cmd, args, what):
	print 'twitter <%s@%s/%s> (%s, %s) (%s)' % (nick, userhost, target, cmd, args, what)
	return False

def veto(irc, nick, userhost, target, cmd, args):
	print 'veto <%s@%s/%s> (%s, %s)' % (nick, userhost, target, cmd, args)
	return False

def info(irc, nick, userhost, target, cmd, args):
	irc.notice(target, 'Quote(s) durch '+config.nick+'!')
	return True

def help(irc, nick, userhost, target, cmd, args):
	irc.notice(target, 'Mögliche Befehle:')
	
	if is_channel(target):
		flag = CMD_CHANNEL
	else:
		flag = CMD_QUERY

	for cmd in msg_triggers:
		if cmd[1] and cmd[2] & flag == flag:
			irc.notice(target, ' oder '.join(cmd[0]) + ' - ' + cmd[1])
	return True

def handle_privmsg(irc, nick, userhost, target, message):
	try:
		cmd, args = message.split(' ', 1)
	except ValueError:
		cmd, args = message, None
	cmd = cmd.lower()

	if is_channel(target):
		flag = CMD_CHANNEL
	else:
		flag = CMD_QUERY

	for trigger in msg_triggers:
		if trigger[2] & flag == flag:
			if cmd in trigger[0]:
				splatargs = trigger[4] if len(trigger) > 4 else []
				kwargs = trigger[5] if len(trigger) > 5 else {}
				if trigger[3](irc, nick, userhost, target, cmd, args, *splatargs, **kwargs):
					return True

	return False

def handle_kick(irc, nick, userhost, target, victim):
	irc.send('JOIN', target)
	return True

def handle_unknown(irc, prefix, command, args):
	print 'UNKNOWN: %s %s %s' % (prefix, command, args)
	return False

def main():
	irc = IRCConnection(server=config.server, port=config.port, password=config.password, nick=config.nick, realname=config.realname, user=config.user, channels=[config.chan])
	irc.on('privmsg', handle_privmsg)
	irc.on('kick', handle_kick)
	irc.on('*', handle_unknown)
	irc.connect()

CMD_CHANNEL = 1
CMD_QUERY = 2

msg_triggers = [
	# triggers, CMD_CHANNEL | CMD_QUERY, func, *args, **kwargs
	[['!info'], None, CMD_CHANNEL, info],
	[['!help'], 'Diese Liste', CMD_CHANNEL | CMD_QUERY, help],
	[['!tweet', '!twitter'], 'Einen Tweet absetzen', CMD_CHANNEL, twitter, ['tweet']],
	[['!reply', '!re'], 'Auf einen Tweet antworten', CMD_CHANNEL, twitter, ['reply']],
	[['!fav', '!favorite', '!favourite'], 'Einen Tweet faven', CMD_CHANNEL, twitter, ['fav']],
	[['!rt', '!retweet'], 'Einen Tweet RTen', CMD_CHANNEL, twitter, ['rt']],
	[['!veto'], 'Veto einlegen', CMD_CHANNEL, veto],
]

if __name__ == "__main__":
	main()
