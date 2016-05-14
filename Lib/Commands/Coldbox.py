class CreateCommand():
    def __init__(self, sublime_command):
        self.caller = sublime_command
        self.inputTitle = "Enter a value"

    def coldbox( self ):
        cmdString = "coldbox create " + self.typeName
        if self.cmdArgs:
            cmdString += " " + self.cmdArgs

        self.caller.executeCommand( cmdString )

    def inputCommand( self, cb ):
        self.caller.show_input_panel(caption=self.inputTitle, on_done=cb)

    def captureAndRun( self, appName ):
        self.cmdArgs = appName
        self.coldbox()

    def app( self ):
        self.inputTitle = "Enter the name of your app:"
        self.typeName = "app"

        self.inputCommand( self.captureAndRun )

    def model( self ):
        self.inputTitle = "Enter a name for your model:"
        self.typeName = "model"

        self.inputCommand( self.captureAndRun )

    def controller( self ):
        self.inputTitle = "Enter a name for your controller:"
        self.typeName = "controller"

        self.inputCommand( self.captureAndRun )

    def interceptor( self ):
        self.inputTitle = "Enter a name for your controller:"
        self.typeName = "interceptor"

        self.inputCommand( self.captureAndRun )

    def view( self ):
        self.inputTitle = "Enter a name for your view"
        self.typeName = "controller"

        self.inputCommand( self.captureAndRun )

    def layout( self ):
        self.inputTitle = "Enter a name for your layout"
        self.typeName = "layout"

        self.inputCommand( self.captureAndRun )

    def entity( self ):
        self.inputTitle = "Enter the name for the ORM entity:"
        self.typeName = "orm-entity"

        self.inputCommand( self.captureAndRun )

    def service( self ):
        self.inputTitle = "Enter the name for the ORM service:"
        self.typeName = "orm-service"

        self.inputCommand( self.captureAndRun )

    def bdd( self ):
        self.inputTitle = "Enter the name for your BDD Test Spec:"
        self.typeName = "bdd"

        self.inputCommand( self.captureAndRun )

    def unit( self ):
        self.inputTitle = "Enter the name for your Unit Test Spec:"
        self.typeName = "unit"

        self.inputCommand( self.captureAndRun )