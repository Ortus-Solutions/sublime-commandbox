import sublime, sublime_plugin
import os
from threading import Thread
import signal, subprocess

is_sublime_text_3 = int(sublime.version()) >= 3000

if is_sublime_text_3:
    from .BaseCommand import BaseCommand, CrossPlatformProcess, ProcessCache, Env
    from .settings import Settings
    from .Lib.ProgressNotifier import ProgressNotifier
    from .Lib.CrossPlatformCodecs import CrossPlatformCodecs
    from .Lib.DirectoryContext import Dir
    from .Lib.Commands import *
else:
    from BaseCommand import BaseCommand, CrossPlatformProcess, ProcessCache, Env
    from settings import Settings
    from Lib.ProgressNotifier import ProgressNotifier
    from Lib.CrossPlatformCodecs import CrossPlatformCodecs
    from Lib.DirectoryContext import Dir
    from .Lib.Commands import *

class CommandboxCommand( BaseCommand ):  	

    def work( self ):
        self.show_output_panel()
        self.activeTask = ()
        self.executeTask( self.task_name )

    def executeTask( self, task_name ):
        self.scopeNamespaces()
        self.activeTask = self.task_name.partition( "_" )
        
        def namespaceNotFound():
            self.appendToMainThreadOutput( "Commandbox Namespace " + self.activeTask[ 0 ] + " Found!" )
    
        def functionNotFound():
            self.appendToMainThreadOutput( "Commandbox Namespace `" + self.activeTask[ 0 ] + "` has no function with the name `" + self.activeTask[ 2 ] + "`.\n" )

        ns = getattr( self, self.activeTask[ 0 ] + "Command", namespaceNotFound )
        fn = getattr( ns, self.activeTask[ 2 ], functionNotFound );
        
        if self.activeTask[ 0 ] == "install":
            ns.run( self.activeTask[ 2 ] )
        elif fn:
            fn()
        else:
            print("No runnable command provided.")

    def scopeNamespaces( self ):
        try:
            getattr( self, "serverCommand" )
        except AttributeError:
            setattr( self, "defaultCommand", self )
            setattr( self, "helpCommand", HelpCommand( self ) )
            setattr( self, "arbitraryCommand", ArbitraryCommand( self ) )
            setattr( self, "serverCommand", ServerCommand( self ) )
            setattr( self, "configCommand", ConfigCommand( self ) )
            setattr( self, "createCommand", CreateCommand( self ) )
            setattr( self, "artifactsCommand", ArtifactsCommand( self ) )
            setattr( self, "forgeboxCommand", Commands.ForgeboxCommand( self ) )
            setattr( self, "testboxCommand", TestboxCommand( self ) )
            setattr( self, "forgeboxCommand", ForgeboxCommand( self ) )
            setattr( self, "installCommand", InstallCommand( self ) )

    def start( self ):
    	self.show_output_panel()
    	self.process.run( self.settings.binary + " server start" )
    	stdout, stderr = self.process.communicate(self.appendToMainThreadOutput)

    def exit( self ):
        if ServerCommand.serverIsRunning:
            ServerCommand.stop();

