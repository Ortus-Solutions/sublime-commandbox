class ServerCommand():
    def __init__(self, sublime_command):
        self.serverIsRunning = False
        self.caller = sublime_command

    def start( self ):
        try:
            self.serverIsRunning
        except AttributeError:
            self.serverIsRunning = False

        self.serverIsRunning = True
        self.caller.executeCommand( "server start" )

    def stop( self ):
        try:
            self.serverIsRunning
        except AttributeError:
            self.serverIsRunning = False

        if self.serverIsRunning:
            self.serverIsRunning=False
            self.caller.executeCommand( "server stop" )