class ArbitraryCommand():
    def __init__(self, sublime_command):
        self.caller = sublime_command

    def input( self ):
        self.caller.show_input_panel(caption="Enter a Commandbox Command", on_done=self.run)

    def run( self,  task_name=None ):
        if task_name:
            self.caller.show_output_panel()
            try: 
                self.caller.executeCommand( task_name.strip() )
            except Exception:
                self.caller.appendToMainThreadOutput(  "Running Command: " + task_name + "\n\n" )