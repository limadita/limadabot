#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

import irc.client
import wikibot
import sys
import random

global PRIV_COMMANDS, PUB_COMMANDS

PRIV_COMMANDS = ["ADD", "REMOVE", "HELP"] 
PUB_COMMANDS = ["!", "HELP"]

class Command:
    def __init__(self, nick, command, iddesc):
        self.command = command
        self.iddesc = iddesc
        self.srcnick = nick
          
def on_connect(connection, event):
    if irc.client.is_channel(target):
        connection.join(target)

    connection.privmsg( target, u"¿Cafecito?" )

def on_join(connection, event):
    pass    


def on_privmsg(connection, event):
    #print(event.source.nick)
    #connection.privmsg( event.source.nick, "Acabas de decirme: " + event.arguments[0] )
    #parse_command( connection, event.source.nick, event.arguments[0] )
    #connection.send_raw( event.arguments[0] )
    parse_command( True, connection, event.source.nick, target, event.arguments[0] )



def on_pubmsg(connection, event):
    print "asi viene:"
    print str( event.arguments )
    parse_command( False, connection, event.source.nick, target, event.arguments[0] )

def on_ison(connection, event):
   data = event.arguments[0].strip();

   if data == "":
       connection.notice( event.source.nick, "User " + data + " not found!" )
       return

   if data in command_queue:
       for i in command_queue[ data ]:
           execute_command( connection, i.srcnick, i.command, data, i.iddesc )

       del command_queue[ data ]

def on_disconnect(connection, event):
    raise SystemExit()

def parse_command( is_private, connection, srcnick, nick, data ):
    print data
    arglist = data.split(" ")

    if len( arglist ) == 1:
        if arglist[0][0] == '!':
            arglist = [ "!", arglist[0].split("!")[1] ]
        else:
            return

    cmd = arglist[0].upper()
    user = arglist[1]
    iddesc = ""

    if cmd == "HELP":
        connection.notice( srcnick, "Ah... no se... arreglatelas..." )
        return
    
    
    
    if cmd == "WIKI":

        definition = wikibot.wikiSearch( arglist[1] )
        print "wiki for " +  arglist[1] +  ":" + definition
        definition = definition.replace( '\r', '' )
        definition = definition.replace( '\n', '' )
        definitionlines = definition.split( '.' )

        definitionlines[0] = arglist[1] + ":" + definitionlines[0]
        
        for line in definitionlines:
            connection.notice( target, line )
            return
        
    if not cmd in PRIV_COMMANDS and not cmd in PUB_COMMANDS: 
        return
    
    if is_private == False and cmd in PRIV_COMMANDS:
        return

    if len(arglist) > 2:
        for i in range( 2, len(arglist) ):
            #print arglist[ i ]
            iddesc += arglist[ i ] + " "

    if user in command_queue:
        command_queue[user].append( Command( srcnick, cmd, iddesc ) )
    else:
        command_queue[user] = [ Command( srcnick, cmd, iddesc ) ]

    connection.ison( [ user ] )


def execute_command( connection, srcnick, cmd, user, iddesc ):
    iddesc = iddesc.strip()
    
    if iddesc.find('\r') != -1 or iddesc.find('\n') != -1:
        iddesc = "Soy un pobre hacker feo :("
        


    elif cmd == "ADD":
        user_ids[ user ] = iddesc
        msg =  "Added ID for " + user + "!. "+ iddesc
        
        connection.notice( srcnick, msg )
        saveFactoids( user_ids )
        
        
    elif cmd == "REMOVE":
        try:
            del user_ids[ user ]
            connection.notice( srcnick, user + " removed from list!" )
        except KeyError:
            connection.notice( srcnick, "ID for " + user + " doesn't exist!" )

    elif cmd == "TELL":
        if user in user_ids:
            connection.privmsg( target, user_ids[ user ] )
        else:
            connection.notice( srcnick, user + " hasn't any id yet! use ADD <nick> <id>" )



def loadFactoids():

    result = {}    
    
    try:
        file = open( "factoids.dat", 'a' )
        file.close()
            
        file = open( "factoids.dat", 'r+' )
           
        factoids_data = file.readlines()
        
        print "LOADING..."
        print str( factoids_data )
        
        if len( factoids_data ) >= 2:
            
            for index in range(0, len(factoids_data) - 1, 2):
                nick = factoids_data[ index ].strip()
                factoid = factoids_data[ index + 1 ].strip()
                result[ nick ] = factoid           

        file.close()
        
        print "LOAD SUCCESS"
            
    except IOError:
        print "LOAD ERROR: Couldn't create factoids.dat :("
    

    return result


def saveFactoids( data_dict ):
    
    try:
        file = open( "factoids.dat", 'w' )
        
        for key in data_dict.keys():

            s = data_dict[ key ]

            if isinstance( s, str ):
                s.decode( 'UTF-8', 'replace' )

            file.write( key + '\n' )
            file.write( s.encode( 'ISO-8859-1' ) + '\n' )
        
        file.close()
        print "SAVE SUCCESS"
    except IOError:
        print "SAVE ERROR: Couldn't create factoids.dat... disk is full?"
        

def main():
    print  "DALE"
    global target
    global user_ids, command_queue
    global file

   
    user_ids = loadFactoids() 
    command_queue = {} 

    #if len(sys.argv) != 4:
    #   print ("Usage: irccat <server[:port]> <nickname> <target>")
    #   print ("\ntarget is a nickname or a channel.")
    #   raise SystemExit(1)

    #cmd, host_port, nickname, target = sys.argv

    cmd = "chat.us.freenode.net"
    host_port = "chat.us.freenode.net:6667"
    nickname = "CoffeeGuy" + str( random.randint(0,1000) ) 
    target = "##roci"
    s = host_port.split(":", 1)

    server = s[0]

    if len(s) == 2:
        
        try:
            port = int(s[1]) 
        except ValueError:
            print "Error: Erroneous port."
            raise SystemExit(1)
    else:
        port = 6667 

    

    print "Connecting"
    
    client = irc.client.IRC() 
    
    try:
        c = client.server().connect(server, port, nickname) 
    except irc.client.ServerConnectionError, x:
        print x 
        raise SystemExit(1)

    print "Connected!"
    
    c.add_global_handler("welcome", on_connect)
    c.add_global_handler("join", on_join)
    c.add_global_handler("disconnect", on_disconnect)
    c.add_global_handler("privmsg", on_privmsg)
    c.add_global_handler("pubmsg", on_pubmsg)
    c.add_global_handler("ison", on_ison)

   
    client.process_forever()



if __name__ == '__main__':
    main()
