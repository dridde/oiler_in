#!/usr/bin/env/python
# -*- coding:utf-8 -*-

import oilib.numreplies

def parse_irc_line(raw):
	parts = raw.strip().split(" ")
	if parts[0][0] == ':':
		# prefixed: pretty much everything
		prefix = parts[0][1:]
		command = parts[1]
		args = parts[2:]
	else:
		# unprefixed: PING etc.
		prefix = None
		command = parts[0]
		args = parts[1:]

	if command.isdigit():
		try:
			command = oilib.numreplies.numerics[command]
		except KeyError:
			print('!!! unknown numeric: %s' % command)

	command = command.upper()

	for idx, arg in enumerate(args):
		if arg[0] == ':':
			args = args[:idx] + [" ".join(args[idx:])[1:]]
			break
	
	return (prefix, command, args)

def parse_prefix(prefix):
	if '!' in prefix:
		nick, userhost = prefix.split('!')
	else:
		nick = prefix
		userhost = None

	return (nick, userhost)

def parse_modes(args):
	"""Parse a mode string, such as:
	
		+b *!*@*.edu +e *!*@*.bu.edu
		+be *!*@*.edu *!*@*.bu.edu
		-l
		+l 25
		-ov+o foo bar moeffju	
	"""
	simple_modes = 'aimnqpsrt'
	complex_modes = 'klbeIOov'

	result = []
	sign = '+'
	for c in args.pop(0):
		if c == '+':
			sign = '+'
		elif c == '-':
			sign = '-'
		else:
			if c in complex_modes and args:
				result.append([sign, c, args.pop(0)])
			else:
				result.append([sign, c, None])
	
	return result

if __name__ == '__main__':
	print '# parse_modes'
	for x in ['+b *!*@*.edu +e *!*@*.bu.edu', '+be *!*@*.edu *!*@*.bu.edu', '-l', '+l 25', '-ov+o foo bar moeffju']:
	  print parse_modes(x.split(' '))
