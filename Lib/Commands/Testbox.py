class TestboxCommand():
    def __init__(self, sublime_command):
        self.caller = sublime_command

    def runnerInput( self ):
        self.caller.show_input_panel(caption="Enter the URL of your Test Runner", on_done=self.run)

    def run( self, runner=None ):
        testCmd = "testbox run"
        if runner:
            testCmd += " runner=" + runner

        self.caller.executeCommand( testCmd )