class ArtifactsCommand():
    def __init__(self, sublime_command):
        self.caller = sublime_command
    
    def clean( self ):
        self.caller.executeCommand( "artifacts clean" )

    def list( self ):
        self.caller.executeCommand( "artifacts list" )

    def remove( self ):
        self.caller.executeCommand( "artifacts list" )