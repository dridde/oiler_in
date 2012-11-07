#!/usr/bin/env python
# -*- coding:utf-8 -*-

from oilib.parse import parse_irc_line, parse_modes, parse_prefix

import sys, socket
#, string, time, datetime, re, random, tweepy, threading

class IRCConnection:
  """Connects to an IRC server and allows you to send and receive messages."""

  def __init__(self, server='localhost', port=6667, password=None, nick=None, realname=None, user=None, channels=[]):
    self.server = server
    self.port = port
    self.password = password
    self.nick = nick
    self.realname = realname
    self.user = user
    self.channels = channels
    self.callbacks = {}

    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  def log_send(self, line):
    print(" -> %s" % line)

  def log_recv(self, line):
    print("<-  %s" % line)

  def sendline(self, line):
    self.log_send(line)
    self.socket.send(line + "\r\n")

  def send(self, *args):
    self.sendline(' '.join([str(x) for x in args]))

  def recv(self, line):
    self.log_recv(line)

  def on(self, command, func):
    if not command in self.callbacks:
      self.callbacks[command.upper()] = []
    self.callbacks[command.upper()].append(func)

  def dispatch(self, prefix, cmd, args, **kwargs):
    lookup_cmd = cmd
    if 'fallback' in kwargs:
      lookup_cmd = '*'

    nick, userhost = parse_prefix(prefix)

    print 'dispatch(prefix="%s", cmd="%s", lookup_cmd="%s")' % (prefix, cmd, lookup_cmd)

    if lookup_cmd in self.callbacks:
      if cmd == 'PRIVMSG' or cmd == 'KICK':
        fargs = [nick, userhost, args[0], ' '.join(args[1:])]

      elif cmd == 'JOIN' or cmd == 'PART':
        fargs = [nick, userhost, args[0]]

      elif cmd == 'MODE':
        modes = parse_modes(args[1:])
        fargs = [nick, userhost, args[0], modes]

      else:
        fargs = [nick, userhost, cmd, args]

      if lookup_cmd == '*':
        fargs = [prefix, cmd, args]

      fargs.insert(0, self)

      for func in self.callbacks[lookup_cmd]:
        print('fargs = %s' % fargs)
        if func(*fargs):
          return True
    return False

  def connect(self):
    self.socket.connect((self.server, self.port))
    # TODO error handling :o
    if self.password:
      self.send('PASS', self.password)
    self.send('NICK', self.nick)
    # 12 = +iw
    self.send('USER', self.user, '12', '*', ':' + self.realname)
    for channel in self.channels:
      self.join(channel)

    try:
      buffer = ''
      while True:
        try:
          buffer += self.socket.recv(1024)
          lines = buffer.split("\n")
          buffer = lines.pop()

          for raw in lines:
            self.recv(raw)

            (prefix, command, args) = parse_irc_line(raw)

            handled = self.dispatch(prefix, command, args)

            if not handled:
              handled &= self.dispatch(prefix, command, args, fallback=True)

            if not handled:
              if command == 'PING':
                self.send('PONG', ':' + args[0])

        except (KeyboardInterrupt, SystemExit):
          print("Caught interrupt, quitting...")
          sys.exit(0)
    finally:
      self.socket.close()

  def join(self, channel, password=None):
    if password:
      self.send('JOIN', channel, password)
    else:
      self.send('JOIN', channel)

  def part(self, channel):
    self.send('PART', channel)

  def privmsg(self, target, message):
    self.send('PRIVMSG', target, ':' + message)

  def notice(self, target, message):
    self.send('NOTICE', target, ':' + message)

