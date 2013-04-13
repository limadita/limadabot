import pluginscore
from pluginscore import plugin_log

import config

#
# Factoids Plugin.
#

class Factoids(pluginscore.Plugin):
    name = "Factoid"

    user_ids = {}
    cfg_filename = "factoids.dat"

    def __init__( self, irc_client, plugin_module ):
        pluginscore.Plugin.__init__( self, irc_client, plugin_module ) 
        plugin_log( "Setting up" )
        Factoids.user_ids = self.load()

        print "PUB = " + str( self.pub_commands )
        print "PRIV = " + str( self.priv_commands )

    def parse( self, commands_array, source, prompt ):

        #Tell short form.
        
        try:
            import re
            args = re.findall( r'!(\w+)', prompt )
            prompt = "Factoid Tell " + args[0]
    
        except:
            pass
        
        pluginscore.Plugin.parse( self, commands_array, source, prompt )
 
    @staticmethod
    def load():
        result = {}    
        
        try:
            file = open( Factoids.cfg_filename, 'a' )
            file.close()
                
            file = open( Factoids.cfg_filename, 'r+' )
               
            factoids_data = file.readlines()
            
            plugin_log( "Loading..." )
            
            if len( factoids_data ) >= 2:
                #Recorre las lineas de a pares
                for index in range(0, len(factoids_data) - 1, 2):
                    nick = factoids_data[ index ].strip()
                    factoid = factoids_data[ index + 1 ].strip()
                    result[ nick ] = factoid           

            file.close()
            
            plugin_log( "Load success!" )
                
        except IOError:
            plugin_log( "LOAD ERROR - Couldn't create factoids.dat :(" )
        

        return result

    @staticmethod
    def save( data_dict ):
        try:
            file = open( Factoids.cfg_filename, 'w' )
            
            for key in data_dict.keys():

                s = data_dict[ key ]

                if isinstance( s, str ):
                    s = s.decode( 'UTF-8', 'replace' )

                file.write( key + '\n' )
                file.write( s.encode( config.encoding ) + '\n' )
            
            file.close()
            plugin_log( "Save success!" )
        except IOError:
            plugin_log( "SAVE ERROR - Couldn't create " + Factoids.cfg_filename + " disk is full?" )


class Add(pluginscore.Command):
    """ Assign a factoid to an online nickname, syntax: Factoid Add <nick> <factoid-text> """
    is_public = True
    is_private = True
    name = "ADD"

    def parse(self, source, prompt):
        args = self.findargs( prompt, 2 )#self.findall( r'(\w+)\s(\w+)\s([\w\s]+)', prompt )
 
        self.args = args[1:]
        self.source = source

        # I want to check if user is online before adding.
        self.irc.ircobj.add_global_handler("ison", self.on_ison)

        self.irc.connection.ison( [ self.args[0] ] )

    def on_ison(self, connection, event):
       self.irc.ircobj.remove_global_handler("ison", self.on_ison)
       data = event.arguments[0].strip();

       if data.find( self.args[0] ) > -1:
           self.execute()
       else:
           self.irc.connection.notice( self.source.nick, "User " + data + " not found!" )

    def execute( self ):
        Factoids.user_ids[ self.args[0] ] = self.args[1]
        self.irc.connection.notice( self.source.nick, self.args[0] + " " + self.args[1] )
        #version con comillas
        #self.irc.connection.notice( self.source, self.args[0] + " \"" + self.args[1] + "\"" )

        Factoids.save( Factoids.user_ids )



class Remove(pluginscore.Command):
    """ Remove a factoid from an online nickname, syntax: Factoid Remove <nick>"""
    is_public = True
    is_private = True
    name = "REMOVE"

    def execute( self ):
        if self.args[0] in Factoids.user_ids:
            del Factoids.user_ids[ self.args[0] ]
            self.irc.connection.notice( self.source.nick, self.args[0] + " succesfully removed from factoid list!." )
            


class Tell(pluginscore.Command):
    """ Tell an user's factoid, syntax: Factoid Tell <nick> """
    is_public = True
    is_private = True
    name = "TELL"

    def execute( self ):
        if self.args[0] in Factoids.user_ids:
            self.irc.connection.privmsg( self.source, self.args[0] + ": " + Factoids.user_ids[ self.args[0] ] )
        else:
            self.irc.connection.notice( self.source.nick, "User " + self.args[0] + " not found!" )
        

