global __pluginname__


__pluginname__ = "None"

def plugin_log( string ):
    print __pluginname__ + ": " + string

def findall( regex, prompt ):
    import re
    result = re.findall( regex, prompt )

    if result == None or result == []:
        raise CommandParseException("Findall failed!" )
    
    result = list( result[0] ) #Tomo el tuple.
    return result

class CommandParseException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
        

class MsgSource:
    def __init__( self, nick, channel='' ):
        self.nick = nick
        self.channel = channel

    def __str__(self):
        if self.channel:
            return self.channel
        else:
            return self.nick

class Plugin:
    """ Plugin's template, to be inherited. """

    name = "NONE" #Name expected by the parser.
    
    def __init__( self, irc_client, plugin_module ):
        self.pub_commands = []
        self.priv_commands = []
        self.irc = irc_client
        
        import inspect
        import sys

        global __pluginname__
        __pluginname__ = self.__class__.__name__

        plugin_log("Initializing...")
        
        for c in inspect.getmembers( sys.modules[ plugin_module ], inspect.isclass ):
            command_cls = c[1]
            if issubclass( command_cls, Command ):
                if command_cls.is_private: self.priv_commands.append( command_cls )
                if command_cls.is_public: self.pub_commands.append( command_cls )
                plugin_log( "Command added! -> " + command_cls.__name__ )

        plugin_log("Done!")


    def parse_priv( self, source, prompt ):
        self.parse( self.priv_commands, MsgSource( source ), prompt )

    def parse_pub( self, source, prompt ):
        self.parse( self.pub_commands, MsgSource( source, self.irc.target ), prompt )

    def parse( self, commands_array, source, prompt ):
        #Separo el primer argumento (el plugin) de todo el resto opcional.
        try:
            args = findall( r'(\w+)(?:\s(.+))?', prompt )

            if args[0].lower() != self.name.lower() or len(args) == 1:
                return
        except:
            return

        for command in commands_array:
            print command
            new_command = command( self.irc )

            try:
                new_command.parse( source, args[1] )
            except CommandParseException:
                continue
            

        


class Command:
    """ Command template, to be inherited. """
    
    name = "DEFAULT"
    is_private = True
    is_public = False
 
    def __init__(self, irc_client):
        self.irc = irc_client
    
    def parse(self, source, prompt):
        args = self.findallargs( prompt )
        self.args = args[1:]
        self.source = source
        
        self.execute()
    
    def execute(self):
        #For testing purposes.
        plugin_log( "Command requested " + self.name )
        self.irc_client.connection.privmsg( self.irc_client.target, self.name + " " + self.args[0] )

    def findallargs( self, prompt ):
        result = prompt.split(' ')

        if len(result) < 1 or result[0].lower() != self.name.lower():
            raise CommandParseException("Can't parse this command!" )

        return result

    def findargs(self, prompt, args_qty=1):
        if args_qty > 0:
            args_exp = ( r'\s(\w+)' * (args_qty - 1) ) + r'\s(.+)'
        else:
            args_exp = r''
            
        return self.findall( r'(\w+)' + args_exp, prompt )
            
    def findall( self, regex, prompt ):
        result = findall( regex, prompt )

        if result[0].lower() != self.name.lower():
            raise CommandParseException("Name comparison failed!" )

        return result
        

