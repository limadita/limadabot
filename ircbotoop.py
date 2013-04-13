#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

# Limada <limada@limada.net>

import sys
#reload(sys)
#sys.getdefaultencoding()
import random
import inspect

#IRC lib
import irc.client

#Limadabot stuff
import wikibot
import pluginscore
import config

class IRCClient(irc.client.SimpleIRCClient):
    """A simple single-server IRC client class.

    This is an example of an object-oriented wrapper of the IRC
    framework.  A real IRC client can be made by subclassing this
    class and adding appropriate methods.

    The method on_join will be called when a "join" event is created
    (which is done when the server sends a JOIN messsage/command),
    on_privmsg will be called for "privmsg" events, and so on.  The
    handler methods get two arguments: the connection object (same as
    self.connection) and the event object.

    Instance attributes that can be used by sub classes:

        ircobj -- The IRC instance.

        connection -- The ServerConnection instance.

        dcc_connections -- A list of DCCConnection instances.
    """
    
    def __init__(self, target):
        irc.client.SimpleIRCClient.__init__(self)
        self.target = target
        self.plugin_list = []

    def on_welcome(self, connection, event):
        if irc.client.is_channel(target):
            connection.join(target)

        connection.privmsg( target, u"Hi!." )

    def on_join(self, connection, event):
        pass    

    def on_privmsg(self, connection, event):
        for plugin in self.plugin_list:
            plugin.parse_priv( event.source.nick, event.arguments[0] )
        

    def on_pubmsg(self, connection, event):
        for plugin in self.plugin_list:
            plugin.parse_pub( event.source.nick, event.arguments[0] )
        

    def on_disconnect(self, connection, event):
        client.connection.disconnect( "Bye bye!" )
        raise SystemExit()

    
   

def main():
    global target
    global file
    

   
    cmd = config.server
    host_port = cmd + ":" + str(config.port)

    nickname = config.nickname 
    target = config.target

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

    print "Connecting to " + cmd + "..."

    global client
    client = IRCClient( target ) 
    
    try:
        client.connect(server, port, nickname) 
    except irc.client.ServerConnectionError, x:
        print x 
        raise SystemExit(1)

    print "Connected!"

    print "Setting up plugins..."

    import plugins
    from plugins import *
    
    for mod in plugins.__all__:

        module_name = "plugins." + mod
        
        for c in inspect.getmembers( sys.modules[ module_name ], inspect.isclass ):
            cls = c[1]
           
            if issubclass( cls, pluginscore.Plugin ):
                client.plugin_list.append( cls( client, module_name ) )
                
    try:
        client.start()
    except KeyboardInterrupt:
        client.connection.privmsg( client.target, u"Bye!." )
        client.connection.disconnect( "K-Lined!" )



if __name__ == '__main__':
    main()

    
