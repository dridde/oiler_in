#!/usr/bin/env/python
# -*- coding:utf-8 -*-

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

	command = command.upper()

	for idx, arg in enumerate(args):
		if arg[0] == ':':
			args = args[:idx] + [" ".join(args[idx:])[1:]]
			break
	
	return (prefix, command, args)

def parse_prefix(prefix):
	nick, userhost = prefix.split('!')

	return (nick, userhost)

def parse_modes(args):
	result = []
	mode = '+'
	idx = 1
	for c in args[0]:
		if c == '+':
			mode = '+'
		elif c == '-':
			mode = '-'
		else:
			result.append([mode, c, args[idx]])
			idx += 1
	
	return result
