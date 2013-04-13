#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pluginscore
from pluginscore import plugin_log
import config
import urlparse
import urllib2
import urllib

class TuringTest(pluginscore.Plugin):

    fool_nick = []
    
    channel = '#ubuntu'
    random_list = []
    
    

    # fool!
    def on_names( self, connection, event ):

        if TuringTest.fool_nick:
            return

        print "I'm back!"

        names = event.arguments[ 2 ].split(" ")
        
        
        for name in names:
            if name[0] != "@" and name != config.nickname:
                TuringTest.random_list.append( name )

        print str( TuringTest.random_list )

        import random
        random.seed()
        for i in range( 5 ):
            TuringTest.fool_nick.append( TuringTest.random_list[ random.randint( 0, len( TuringTest.random_list ) - 1 ) ] )

        print "fools nicks are... " + str( TuringTest.fool_nick )

        for fool in TuringTest.fool_nick:
            self.irc.connection.privmsg( fool, self.args[0].strip() )

        self.irc.connection.part( TuringTest.channel )
        
        
        pass

    def on_join( self, connection, event ):
        print "Joined!"
        self.irc.connection.names( [ TuringTest.channel ] )
        self.irc.ircobj.add_global_handler("namreply", self.on_names)
        self.irc.ircobj.remove_global_handler("join", self.on_join)
        pass

    def parse( self, commands_array, source, prompt ):

        import time
        # si el random me habla, lo digo por el channel
        if TuringTest.fool_nick and source in TuringTest.fool_nick:
            TuringTest.fool_nick = [ source ]
            self.irc.connection.privmsg( self.irc.target, prompt )
            print "he said " + prompt
            return
        
        try:
            import re
            self.args = re.findall( config.nickname + r'[:,.\s]?(.+)', prompt )
        except:
            return

        if len( self.args ) == 0:
            return

        print self.args[0].strip()

        if not TuringTest.fool_nick:
            #primera vez, busco un random y le hablo
            self.irc.connection.join( TuringTest.channel )
            self.irc.ircobj.add_global_handler("join", self.on_join)
        else:
            #segunda vez! ya tengo un random. le hablo.
            for fool in TuringTest.fool_nick:
                self.irc.connection.privmsg( fool, self.args[0].strip() )
    

        
"""
        for url in args:

            try:
                hostname = urlparse.urlparse( url ).hostname

                plugin_log( "Parsing " + url )
            
                sock = urllib2.urlopen( url, None, 5 )
                content = sock.read()
            except ValueError:
                             continue
            
            except Exception, x:
                
                plugin_log( "Connection error to: " + url )
                plugin_log( str(x) )
                
                if hostname:
                    self.irc.connection.notice( source, "ERROR: " + str(x) + " (at " + hostname + ") " )
                else:
                    self.irc.connection.notice( source, "ERROR: " + str(x) )
                    
                continue

            title = re.findall( r'<title>(.+?)</title>', content )

            if len(title) > 0:
                title = title[0]

                if isinstance( title, str ):
                    title = unicode( title.decode( "UTF-8", "replace" ) )
                
                #print "TITLE = " + title + " (at " + hostname + ") "
                self.irc.connection.privmsg( source, title + " (at " + hostname + ") " )
       """


