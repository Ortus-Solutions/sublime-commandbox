class ForgeboxCommand():
    def __init__(self, sublime_command):
        self.caller = sublime_command

    def inputLogin( self ):
        self.caller.show_input_panel(caption="Enter your Forgebox Username:", on_done=self.inputPassword)

    def inputPassword( self, username=None ):
        print( "Username: " + username )
        if username:
            self.username = username
            self.caller.show_input_panel(caption="Enter your Password:", on_done=self.login)

    def inputSearch( self ):
        self.caller.show_input_panel(caption="Enter a search term", on_done=self.search)

    def search( self, term=None ):
        if term:
            self.caller.executeCommand( "forgebox search '" + term + "'" )

    def publish( self ):
        self.caller.executeCommand( "forgebox publish" )

    def login( self, runner=None ):
        testCmd = "testbox run"
        if runner:
            testCmd += " runner=" + runner

        self.caller.executeCommand( testCmd )