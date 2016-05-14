class HelpCommand():
    def __init__(self, sublime_command):
        self.caller = sublime_command

    def run( self, namespace="" ):
        helpCommand = namespace + " help"
        self.caller.executeCommand( helpCommand.strip() )

    def install( self ):
        self.run( "install" )

    def create( self ):
        self.run( "coldbox create" )

    def server( self ):
        self.run( "server" )

    def testbox( self ):
        self.run( "testbox" )