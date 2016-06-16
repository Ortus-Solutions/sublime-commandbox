class InstallCommand():
    def __init__(self, sublime_command):
        self.caller = sublime_command

    def run( self, packageName ):
    	if packageName == 'arbitrary':
    		self.caller.show_input_panel(caption="Enter a Forgebox Package to Install", on_done=self.run)
    	else:
        	self.caller.executeCommand( "install " + packageName )
