#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pluginscore
from pluginscore import plugin_log
import config
import urlparse
import urllib2
import urllib

#
# DetectURL Plugin - Detects any URL input in the IRC target
#                    and provides some insight about it.
#

FORBIDDEN_PATTERNS = [ '127.0.0.1', 'localhost', '192.168' ]
WARNINGS_LIMIT = 5
FLOOD_TIME_THRESHOLD = 1.0


# User warnings, flooding, punish data
class Dossier:
    def __init__(self, nick):
        self.nick = nick
        self.last_msg_time = 0
        self.warnings = 0
        self.unlock_time = 0 # if > 0 user is ignored until time > unlock_time.

    def punish( self, minutes ):
        plugin_log( "Punishing " + self.nick + "... by %i minutes" % (minutes,) )

        from time import time
        self.unlock_time = time() + ( 60 * minutes )
        self.warnings = 0

    def add_warning( self, punishment ):
        self.warnings += 1

        plugin_log( "Adding warning to " + self.nick + "... Warning level: %i " % (self.warnings, ) )

        if self.warnings > WARNINGS_LIMIT:
            self.punish( punishment )
            return True

        return False
        
        


class DetectURL(pluginscore.Plugin):
    name = "DetectURL"

    def __init__( self, irc_client, plugin_module ):
        pluginscore.Plugin.__init__( self, irc_client, plugin_module )
        self.dossiers = {}

    def get_dossier( self, nick ):
        if not nick in self.dossiers:
            self.dossiers[ nick ] = Dossier( nick )

        return self.dossiers[ nick ]

    def on_punish( self, source, punishment ):
        self.irc.connection.notice( self.irc.target, "Ok! " + source.nick + ", por hacerte el vivo, " + str(punishment) + " minutos de ignore." )

    def parse( self, commands_array, source, prompt ):

        #Security measures!
        from time import time

        dossier = self.get_dossier( source.nick )

        if dossier.unlock_time > time():
            return

        try:
            import re
            args = re.findall( r'(?P<url>https?://[^\s]+)', prompt )
        except:
            return


        if time() - dossier.last_msg_time < FLOOD_TIME_THRESHOLD:
            if dossier.add_warning( 10 ):
                self.on_punish( source, 10 )
                return
        

        for url in args:

            try:
                for forbidden_string in FORBIDDEN_PATTERNS:
                    if url.lower().find( forbidden_string ) > -1:
                         dossier.punish( 5 )
                         self.on_punish( source, 5 )
                         return
                        
                hostname = urlparse.urlparse( url ).hostname

                plugin_log( "Parsing " + url )
            
                sock = urllib2.urlopen( url, None, 5 )
                content = sock.read()
            except ValueError, x:
                plugin_log( str(x) )
                continue
            
            except Exception, x:
                
                plugin_log( "Connection error to: " + url )
                plugin_log( str(x) )
                
                if hostname:
                    self.irc.connection.notice( source.nick, "ERROR: " + str(x) + " (at " + hostname + ") " )
                else:
                    self.irc.connection.notice( source.nick, "ERROR: " + str(x) )

                if dossier.add_warning( 10 ):
                    self.on_punish( source, 10 )
                    return

                continue

            title = re.findall( r'<title>(.+?)</title>', content )

            if len(title) > 0:
                title = title[0]

                if isinstance( title, str ):
                    title = unicode( title.decode( "UTF-8", "replace" ) )
                
                #print "TITLE = " + title + " (at " + hostname + ") "
                self.irc.connection.privmsg( source, title + " (at " + hostname + ") " )

                if dossier.warnings > 0:
                    dossier.warnings -= 1
                


