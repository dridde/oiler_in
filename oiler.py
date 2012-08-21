#!/usr/bin/env python
# -*- coding:Utf-8 -*-
import sys, socket, string, time, datetime, urllib, re, random, tweepy, threading

# MetaKram

#Username der schreibt
def getName(line, forIgnore = False):
	try:
		if (forIgnore == False):
			return str( line[0][1:line[0].index("!")])
		else:
			return str(line[4])
	except:
		return -1

#Channel aus dem es kam
def getChannel(line, forIgnore=False):
	try:
		if (forIgnore == False):
			if (line[2] == nick):
				return -1
			else:
				return str(line[2])
		else:
			if (line[2] == nick):
				return str(line[5])
	except:
		return -1

#Passwort fuer ignore
def getPassword(line, position = 6):
	try:
		return str(line[position])
	except:
		return -1

def isQuery(line):
	try:
		if (line[2] == nick):
			return True
		else:
			return False
	except:
		return False

# sende kommandos
def send(type, msg, irc):
	if (type == "NICK"):
		irc.send("Nick " + msg + "\r\n")
		#nick = msg
	elif (type == "USER"):
		irc.send("USER " + nick + " " + nick + " " + nick + " :"+ nick + "\r\n")
	elif (type == "JOIN"):
		irc.send("JOIN " + msg + "\r\n")
	elif (type == "QUIT"):
		irc.send("QUIT\r\n")
	elif (type == "IDENT"):
		irc.send("PRIVMSG NICKSERV :identify" + str(msg) + "\r\n")
	else:
		irc.send("PRIVMSG " + chan + " :" + str(msg) + "\r\n")

# sende normale channelnachricht
def sendpriv(line, msg, irc):
	if (isQuery(line) == True):
		irc.send("PRIVMSG " + getName(line) + " :" + str(msg) + "\r\n")
	else:
		irc.send("PRIVMSG " + getChannel(line) + " :" + str(msg) + "\r\n")


def checkQueryPW(line, position = 6):
	if (isQuery(line) == True):
		if (getPassword(line, position) == ownerpw):
			return True
		else:
			sendpriv(line, "Falsches PW", irc)
	else:
		sendpriv(line, "Das solltest du lieber im Query tun!", irc)
	return False

# ende MetaKram

# User ignorieren
def ignore(line):
	if (isQuery(line) == True):
		if (getChannel(line, True) != -1) :
			# ignore-Liste pro Channel öffnen/anlegen
			rhandle = open("./ignored_"+getChannel(line, True)+".txt", "r")
			ignored = rhandle.read()
			rhandle.close()
		
			# ignore-Liste zum schreiben öffnen
			whandle = open("ignored_"+getChannel(line, True)+".txt", "w")
		
			if (ignored.count(line[4]) > 0):
				output = ignored.replace(line[4], "")
				whandle.write(output)
				# optional message
				sendpriv(line, str(line[4]) + " wird in "+getChannel(line, True)+" von mir nicht mehr ignoriert.", irc)
			else:
				write = ignored + str(line[4])
				whandle.write(write)
				sendpriv(line, str(line[4]) + " wird in "+getChannel(line, True)+" von mir ab jetzt ignoriert.", irc)
			whandle.close()
		else:
			sendpriv(line, "Kein gültiger Channel angegeben", irc)
	else:
		sendpriv(line, "Das solltest du besser im Query tun!", irc)

def isIgnored(line):
	if (getChannel(line) != -1):
		iusers = open("./ignored_"+getChannel(line)+".txt", "a+")
		ignored_users = iusers.read()
		iusers.close()
	
		if (ignored_users.count(getName(line)) > 0):
			return True
		else:
			return False
	else:
		return False

# ende User ignorieren

# quote handling

def getQuoteCount(line):
	if (isQuery(line) == False):
		if (getChannel(line, True) != -1) :
			try:
				# quote-Liste pro Channel öffnen/anlegen
				counter = 0
				rhandle = open("./quotes_"+getChannel(line)+".txt", "r")
				for line in rhandle:
					counter += 1
				rhandle.close()
				return counter
			except:
				return 0

def addQuote(line):
	if (isQuery(line) == False):
		filetxt = open('./quotes_'+getChannel(line)+'.txt', 'a+')
		message = ' '.join(line[4:])
		#now = datetime.datetime.now()
		#filetxt.write((getName(line)) + '\n')
		#filetxt.write(now.strftime("%Y-%m-%d %H:%M") + '\n')
		filetxt.write(string.lstrip(message, ':') + '\n')
		filetxt.flush()
		filetxt.close()
		sendpriv(line, "Quote Nr. " + str(getQuoteCount(line)) + " hinzugefügt.", irc)
	else:
		sendpriv(line, "Das geht im Query nicht!", irc)

def getQuote(line):
	if (isQuery(line) == False):
		nr = getQuoteNr(line)
		quoteCount = getQuoteCount(line)
		if (quoteCount == 0):
			sendpriv(line, "Noch keine Quotes gespeichert", irc)
			return
		if (nr == -1 and quoteCount != 1):
			nr = random.randrange(1, quoteCount)
		elif (nr > quoteCount):
			sendpriv(line, "Dieses Zitat existiert noch nicht", irc)
			return
		elif (quoteCount == 1):
			nr = 1

		rhandle = open("./quotes_"+getChannel(line)+".txt", "r")
		counter = 0
		for quotes in rhandle:
			counter += 1
			if (counter == nr):
				sendpriv(line, string.strip(quotes), irc)
		rhandle.close()
	else:
		sendpriv(line, "Das geht im Query nicht!", irc)

def getQuoteNr(line):
	try:
		return int(line[4])
	except:
		return -1


def getQuoteInfo(line):
	if (isQUery(line) == False):
		sendpriv(line, "Das geht im Query nicht!", irc)
	else:
		sendpriv(line, "Das geht im Query nicht!", irc)

def delQuote(line):
	if (isQuery(line) == False):
		nr = getQuoteNr(line)
		quoteCount = getQuoteCount(line)
		if (quoteCount == 0):
			sendpriv(line, "Noch keine Quotes gespeichert", irc)
			return
		elif ((nr > quoteCount) or (nr <= 0)):
			sendpriv(line, "Dieses Zitat existiert nicht", irc)
			return

		handle = open("./quotes_"+getChannel(line)+".txt", "r")
		quotelist = []
		for quotes in handle:
			quotelist.insert(0, quotes)
		handle.close()
		del quotelist[nr-1]
		
		filetxt = open('./quotes_'+getChannel(line)+'.txt', 'w')
		while (len(quotelist) > 0):
			filetxt.write(quotelist.pop())
		filetxt.flush()
		filetxt.close()
		sendpriv(line, "Quote Nr. " + str(nr) + " gelöscht.", irc)
	else:
		sendpriv(line, "Das geht im Query nicht!", irc)

# ende quote handling

# twitter kram
def tweetIt(line):
	if (isQuery(line) == False):
		try:
			message = ' '.join(line[4:])
			if (len(message) > 140):
				sendpriv(line, "Ähem. Der Text ist zu lang.", irc)
			else:
				api.update_status(message)
				sendpriv(line, "Tweet ist raus.", irc)
		except: 
			sendpriv(line, "Ohne Worte...", irc)	
	else:
		sendpriv(line, "Musst schon öffentlich twittern ;)", irc)
# ende twitter kram


# check auf kommandos
def cmd(command, line):
	if (isIgnored(line) == False):
		
		if (command == "!quit"):
			if (checkQueryPW(line, 4) == True):
				send("QUIT", "", irc)
				sys.exit()
		
		elif (command == "!nick"):
			if (checkQueryPW(line, 5) == True):
				global nick
				nick = str(line[4])
				send("NICK", str(line[4]), irc)

		elif (command == "!join"):
			if (checkQueryPW(line, 5) == True):
				send("JOIN", str(line[4]), irc)

		elif (command == "!part"):
			if (checkQueryPW(line, 5) == True):
				send("PART", str(line[4]), irc)		
		elif (command == "!say"):
			if (checkQueryPW(line, 4) == True):
				irc.send("PRIVMSG " + str(line[5]) + " :" + ' '.join(line[6:]) + "\r\n")

		elif (command == "!time"):
			now = datetime.datetime.now()
			sendpriv(line, now.strftime("%Y-%m-%d %H:%M"), irc)
			
		elif (command == "!tweet"):
			tweetIt(line)
		
		elif (command == "!info"):
			sendpriv(line, "Quote(s) durch " + nick +"!", irc)
		
		elif (command == "!help"):
			sendpriv(line, "Mögliche Befehle:", irc)
			sendpriv(line, "!help - diese Commandliste", irc)
			#sendpriv(line, "!info - ein kurzer Infotext", irc)
			sendpriv(line, "!addquote <Text> - Text als Zitat hinzufügen", irc)
			sendpriv(line, "!quote -  zufälliges Zitat ausgeben", irc)
			sendpriv(line, "!quote <nummer> -  Zitat ausgeben", irc)
			#sendpriv(line, "!quoteinfo <nummer> -  Infos zu Zitat ausgeben", irc)
			sendpriv(line, "!delquote <nummer> -  Zitat löschen", irc)
			sendpriv(line, "!ignore <nickname> <channel> <password> - Nur im Query. Nutzer von Botbenutzung ausschließen bzw wieder zulassen", irc)
			sendpriv(line, "!time - Systemzeit ausgeben", irc)
			sendpriv(line, "!tweet <Text> - sendet den String mit dem #nodrama.de Account direkt an Twitter", irc)
		
		elif (command == "!ignore"):
			if (checkQueryPW(line, 6) == True):
				if (getChannel(line, True) != -1 and getName(line, True) != -1):
					ignore(line)
				else:
					sendpriv(line, "Kein Channel oder Nutzer angegeben", irc) 
		
		elif (command == "!addquote"):
			addQuote(line)
		elif (command == "!quote"):
			getQuote(line)		
		elif (command == "!quoteinfo"):
			getQouteInfo(line)
		elif (command == "!delquote"):
			delQuote(line)
		
	else:
		sendpriv(line, "Du nicht!", irc)

# ende kommandocheck 

# main-loop

network = ""
port = 6667
nick = ""
chan = ""
buffer = ""
ownerpw = ""

consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

irc = socket.socket( )
irc.connect((network, port))
send("NICK", nick, irc)
send("USER", "", irc)
send("JOIN", chan, irc)
#send("IDENT", "identify " + password, irc)

#start twitter lausche-thread
def twitterLurk():
	while 1:
		try:
			time.sleep(60)
			mentions = api.mentions();
			for status in mentions:
				if (status.created_at > datetime.datetime.utcnow()-datetime.timedelta(minutes=1)):
					irc.send("PRIVMSG " + chan + " :" + "Tweet von " + str("@" + status.author.screen_name) + ": " + str(status.text) + "\r\n")
		except:
			pass

t = threading.Thread(target=twitterLurk)
t.start()

while 1:
	try:
		buffer = buffer + irc.recv(1024)
		newlines = string.split(buffer, "\n")
		buffer = newlines.pop( )
		
	except:
		sys.exit()
	
	for line in newlines:
		line = string.rstrip(line)
		line = string.split(line)
		#output = " ".join(line)
		#print output
		
		
		try:
			if (line[3][1] == "!"):
				cmd(line[3][1:], line)
				
		except(IndexError):
			pass
		
		# send pong gemäß RFC 1459 falls angefordert
		if (line[0] == "PING"):
			irc.send("PONG %s\r\n" % line[1])
		
		# rejoin nach kick
		if (line[1] == "KICK" and line[3] == nick):
			send("JOIN", line[2], irc)
