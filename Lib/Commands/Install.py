class InstallCommand():
    def __init__(self, sublime_command):
        self.caller = sublime_command

    def run( self, packageName ):
        self.caller.executeCommand( "install " + packageName )
