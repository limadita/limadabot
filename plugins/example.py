import pluginscore
from pluginscore import plugin_log

import config

#
# Example Plugin - It has some random commands to help learn to write plugins.
#

class Example(pluginscore.Plugin):
    """ It has some random commands to help learn to write plugins. """
    name = "Example"

class Hello(pluginscore.Command):
    """ Prints 'hello world!' as a notice to the irc caller """

    # Command responds when used in channel?
    is_public = True 

    # Command responds when used in a query?
    is_private = True 

    # Command name in IRC (not case sensitive)
    name = "HELLO" 

    # This is called by Command.parse when the command is received.
    def execute( self ):
       self.irc.connection.notice( self.irc.target, "Hello world!" )

class Eval(pluginscore.Command):
    """ Eval any expression, syntax: Example Eval <expression> """
    is_public = True
    is_private = True
    name = "EVAL"

    # This is directly called by the IRC client everytime ANYTHING
    # is written, it -usually- returns if command name or args count
    # doesn't match.
    # But not necesarilly this has to be the case.
    #
    # This method is responsible for parsing any prompt and calling
    # Command.execute
    def parse(self, source, prompt):

        # Command.findall is cleaner than re.findall.
        # It returns the () regex groups as a list and makes sure the
        # command name matches. 

        # If it fails, it'll raise a CommandParseException handled by the plugin.
        args = self.findall( r'(\w+)\s(.+)', prompt )


        # Strip command name from args
        self.args = args[1:]

        # Save the caller for future use.
        self.source = source
        
        self.execute()
 
    def execute( self ):
        try:
            self.irc.connection.notice( self.irc.target, "Result is " + str( eval( self.args[0] ) ) + "!." )
        except:
            self.irc.connection.notice( self.irc.target, "Bad expression!" )
        
