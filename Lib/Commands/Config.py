class ConfigCommand():
    def __init__(self, sublime_command):
        self.caller = sublime_command

    def inputGet( self ):
        self.caller.show_input_panel(caption="Enter Configuration Key For Lookup:", on_done=self.getConfig)

    def inputSet( self ):
        self.caller.show_input_panel(caption="Enter Configuration Key:", on_done=self.input2)

    def input2( self, configKey=None ):
        if configKey != None:
            self.configKey = configKey
            self.caller.show_input_panel(caption="Enter ConfigurationValue:", on_done=self.setConfig)

    def getConfig( self, configKey=None ):
        if configKey != None:
            self.caller.show_output_panel( "Getting config key: " + configKey )
            self.caller.executeCommand( "config show " + configKey )

    def setConfig( self, configValue=None ):
        if self.configKey and configValue != None:
            self.caller.executeCommand( "config set " + self.configKey + "=" + configValue )