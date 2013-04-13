import pluginscore
from pluginscore import plugin_log

import config

import memebot

#
# MemeGenerator Plugin.
#

class Meme(pluginscore.Plugin):
    name = "Meme"

class List(pluginscore.Command):
    """ Assign a factoid to an online nickname, syntax: Factoid Add <nick> <factoid-text> """
    is_public = True
    is_private = True
    name = "List"

    def execute( self ):
        #url = memebot.makeMeme( self.args[0], self.args[1], self.args[2] )
        self.irc.connection.privmsg( self.source, "Available meme images: " + str( memebot.images.keys() ) )


class Make(pluginscore.Command):
    """ Assign a factoid to an online nickname, syntax: Factoid Add <nick> <factoid-text> """
    is_public = True
    is_private = True
    name = "10Guy"

    def parse(self, source, prompt):
        # saca 10Guy <exp> <exp> o bien 10Guy "<exp>" "<exp>"
        args = pluginscore.findall( r'^(\w+)\s(?:"(.+)"\s"(.+)"|(\w+)\s(\w+))$', prompt )

        if args[0].lower() == "list":
            raise CommandParseException("Name comparison failed!" )
        
        # convierte los resultados de más a 2 solos (regexp fail)
        args = [ args[0], args[1] + args[3], args[2] + args[4] ]
         
        self.args = args
        self.source = source

        self.execute()

    def execute( self ):
        url = memebot.makeMeme( self.args[0], self.args[1], self.args[2] )
        self.irc.connection.notice( self.irc.target, url )


