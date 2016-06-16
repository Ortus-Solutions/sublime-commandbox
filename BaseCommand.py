import sublime, sublime_plugin
import os
import os.path
from threading import Thread
import signal, subprocess
import shutil

is_sublime_text_3 = int(sublime.version()) >= 3000

if is_sublime_text_3:
    from .settings import Settings
    from .Lib.ProgressNotifier import ProgressNotifier
    from .Lib.CrossPlatformCodecs import CrossPlatformCodecs
    from .Lib.DirectoryContext import Dir
else:
    from settings import Settings
    from Lib.ProgressNotifier import ProgressNotifier
    from Lib.CrossPlatformCodecs import CrossPlatformCodecs
    from Lib.DirectoryContext import Dir

# A base for each command
class BaseCommand(sublime_plugin.WindowCommand):
    package_name = "Commandbox"
    
    def run(self, task_name=None, task_flag=None, silent=False, paths=[]):
        self.searchable_folders = [os.path.dirname(path) for path in paths] if len(paths) > 0 else self.window.folders()
        self._working_dir = ""
        self._working_dir = self.projectPath()
        print( "Working Directory: " + self._working_dir )
        self.settings = Settings()
        self.setup_data_from_settings()
        
        self.process = CrossPlatformProcess( self )
        self.non_blocking=False
        self.results_in_new_tab=False
        self.task_name = task_name
        self.task_flag = task_flag if task_name is not None and task_flag is not None else self.get_flag_from_task_name()
        self.silent = silent
        self.output_view = self.window.get_output_panel("commandbox_output")
        
        self.work()

    def setup_data_from_settings(self):
        self.results_in_new_tab = self.settings.get("results_in_new_tab", False)
        self.nonblocking  = self.settings.get("nonblocking", True)
        self.exec_args = self.settings.get('exec_args', False)


    def get_flag_from_task_name(self):
        flags = self.settings.get("flags", {})
        return flags[self.task_name] if self.task_name in flags else ""

    def executeCommand( self, cmd ):
        try:
            self.settings.binary
        except AttributeError:
            binaryPath = self.findBinaryPath( "box" )
            if binaryPath:
                self.settings.binary = os.path.join(binaryPath)
            else:
                self.appendToMainThreadOutput( "A CommandBox binary could not be found to run.  Please set the binary path in your user settings or install CommandBox first." )
                return False

        print( "Binary: " + self.settings.binary + "\n" )
        print( "Commandbox is ready:" + str(self.isCommandboxReady()) + "\n" )

        # if not self.isCommandboxReady():
        self.show_panel()
        binaryCmd = self.settings.binary + " " + cmd
        self.process.run( binaryCmd )
        stdout, stderr = self.process.communicate(self.appendToMainThreadOutput)

    def findBinaryPath( self, binaryName ):
        # If we have a commandbox installation in our project root:
        if os.path.isfile( self.working_dir + '/' + binaryName ):
            return self._working_dir + '/' + binaryName
        elif os.path.isfile( '/usr/bin/' + binaryName):
            return '/usr/bin/' + binaryName
        elif os.path.isfile( '/usr/sbin/' + binaryName):
            return '/usr/sbin/' + binaryName
        elif os.path.isfile( '/usr/local/bin/' + binaryName):
            return '/usr/local/bin/' + binaryName
        else:
            return shutil.which( binaryName )

    def isCommandboxReady( self ):
        return self.process.is_alive()

    def projectPath( self ):
        return self.searchable_folders[ 0 ]
        # next(folder_path for folder_path in self.searcheable_folders if self.working_dir.find(folder_path) != -1) if self.working_dir else ""

    # Properties
    @property
    def working_dir(self): 
        return self._working_dir

    @working_dir.setter
    def working_dir(self, value): 
            self._working_dir = os.path.dirname(value)
        
    # Main method, override
    def work(self):
        pass

    # Panels and message
    def show_quick_panel(self, items, on_done=None, font=sublime.MONOSPACE_FONT):
        self.defer_sync(lambda: self.window.show_quick_panel(items, on_done, font))

    def show_input_panel(self, caption, initial_text="", on_done=None, on_change=None, on_cancel=None):
        self.window.show_input_panel(caption, initial_text, on_done, on_change, on_cancel)

    def status_message(self, text):
        sublime.status_message("%s: %s" % (self.package_name, text))

    def error_message(self, text):
        sublime.error_message("%s: %s" % (self.package_name, text))

    # Output view
    def show_output_panel(self, text=''):
        if self.silent:
            self.status_message(text)
            return
        
        if self.results_in_new_tab:
            new_tab_path = os.path.join(self.commandbox_results_path(), "Commandbox Results")
            self.output_view = self.window.open_file(new_tab_path)
            self.output_view.set_scratch(True)
        else:
            self.output_view = self.window.get_output_panel("commandbox_output")
            self.show_panel()
            
        self.output_view.settings().set("scroll_past_end", False)
        self.add_syntax()
        self.appendToOutput(text)

    def commandbox_results_path(self):
        return next(folder_path for folder_path in self.searchable_folders if self.working_dir.find(folder_path) != -1) if self.working_dir else ""

    def commandbox_results_view(self):
        if self.output_view is None:
            commandbox_results = [view for view in sublime.active_window().views() if view.file_name() and os.path.basename(view.file_name()) == "Gulp Results"]
            return commandbox_results[0] if len(commandbox_results) > 0 else None
        else:
            return self.output_view

    def add_syntax(self):
        if self.settings.has("syntax_override"):
            syntax_file = self.settings.get("syntax_override")
        else:
            syntax_file = self.settings.get_from_user_settings("syntax", "Packages/Gulp/syntax/GulpResults.tmLanguage")
            
        if syntax_file:
            self.output_view.set_syntax_file(syntax_file)

    def appendToMainThreadOutput(self, text):
        self.defer_sync(lambda: self.appendToOutput(text))

    def appendToOutput(self, text):
        if not self.silent:
            decoded_text = text if is_sublime_text_3 else CrossPlatformCodecs.force_decode(text)
            self._insert(self.output_view, decoded_text)

    def _insert(self, view, content):
        if view is None:
            return

        if self.results_in_new_tab and view.is_loading():
            self.set_timeout(lambda: self._insert(view, content), 15)
        else:
            view.set_read_only(False)
            view.run_command("view_insert", { "size": view.size(), "content": content })
            view.set_viewport_position((0, view.size()), True)
            view.set_read_only(True)

    def setOutputCloseOnTimeout(self):
        timeout = self.settings.get("results_autoclose_timeout_in_milliseconds", False)
        if timeout:
            self.set_timeout(self.close_panel, timeout)

    def close_panel(self):
        if self.results_in_new_tab:
            self.output_view = self.commandbox_results_view()
            if self.output_view and self.output_view.file_name():
                self.window.focus_view(self.output_view)
                self.window.run_command('close_file')
        else:
            self.window.run_command("hide_panel", { "panel": "output.commandbox_output" })

    def show_panel(self):
        self.window.run_command("show_panel", { "panel": "output.commandbox_output" })

    # Sync/async calls
    def defer_sync(self, fn):
        self.set_timeout(fn, 0)

    def defer(self, fn):
        self.async(fn, 0)

    def set_timeout(self, fn, delay):
        sublime.set_timeout(fn, delay)
        
    def async(self, fn, delay):
        if is_sublime_text_3:
            progress = ProgressNotifier("Commandbox: Running...\n\n")
            sublime.set_timeout_async(lambda: self.call(fn, progress), delay)
        else:
            fn()

    def call(self, fn, progress):
        fn()
        progress.stop()


class ViewInsertCommand(sublime_plugin.TextCommand):
    def run(self, edit, size, content):
        self.view.insert(edit, int(size), content)

#
# General purpose Classes.
#

class CrossPlatformProcess():
    def __init__(self, sublime_command):
        self.working_dir = sublime_command.working_dir
        self.nonblocking = sublime_command.nonblocking
        self.path = Env.get_path(sublime_command.exec_args)
        self.last_command = ""
        self.failed = False

    def run(self, command):
        with Dir.cd(self.working_dir):
            self.process = subprocess.Popen([command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=self.path, shell=True, preexec_fn=self._preexec_val())

        self.last_command = command
        ProcessCache.add(self)
        return self

    def run_sync(self, command):
        command = CrossPlatformCodecs.encode_process_command(command)

        with Dir.cd(self.working_dir):
            self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=self.path, shell=True)
            (stdout, stderr) = self.process.communicate()
            self.failed = self.process.returncode == 127 or stderr

        return (CrossPlatformCodecs.force_decode(stdout), CrossPlatformCodecs.force_decode(stderr))

    def _preexec_val(self):
        return os.setsid if sublime.platform() != "windows" else None

    def communicate(self, fn = lambda x:None):
        stdout, stderr = self.pipe(fn)
        self.process.communicate()
        # self.terminate()
        return (stdout, stderr)

    def pipe(self, fn):
        streams = [self.process.stdout, self.process.stderr]
        streams_text = []
        if self.nonblocking:
            threads = [ThreadWithResult(target=self._pipe_stream, args=(stream, fn)) for stream in streams]
            [t.join() for t in threads]
            streams_text = [t.result for t in threads]
        else:
            streams_text = [self._pipe_stream(stream, fn) for stream in streams]
        return streams_text

    def _pipe_stream(self, stream, fn):
        output_text = ""
        while True:
            line = stream.readline()
            if not line: break
            output_line = CrossPlatformCodecs.decode_line(line)
            output_text += output_line
            fn(output_line)
        return output_text

    def terminate(self):
        if self.is_alive():
            self.process.terminate()
        ProcessCache.remove(self)

    def is_alive(self):
        try:
            return self.process.poll() is None
        except AttributeError:
            return False

    def returncode(self):
        return self.process.returncode

    def kill(self):
        pid = self.process.pid
        if sublime.platform() == "windows":
            kill_process = subprocess.Popen(['taskkill', '/F', '/T', '/PID', str(pid)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            kill_process.communicate()
        else:
            os.killpg(pid, signal.SIGTERM)
        ProcessCache.remove(self)


class ProcessCache():
    _procs = []

    @classmethod
    def add(cls, process):
       cls._procs.append(process)

    @classmethod
    def remove(cls, process):
        if process in cls._procs:
            cls._procs.remove(process)

    @classmethod
    def kill_all(cls):
        cls.each(lambda process: process.kill())
        cls.clear()

    @classmethod
    def each(cls, fn):
        for process in cls._procs:
            fn(process)

    @classmethod
    def empty(cls):
        return len(cls._procs) == 0

    @classmethod
    def clear(cls):
        del cls._procs[:]


class Env():
    @classmethod
    def get_path(self, exec_args=False):
        env = os.environ.copy()
        if exec_args:
            path = str(exec_args.get('path', ''))
            if path:
                env['PATH'] = path
        return env


class ThreadWithResult(Thread):
    def __init__(self, target, args):
        self.result = None
        self.target = target
        self.args = args
        Thread.__init__(self)
        self.start()

    def run(self):
        self.result = self.target(*self.args)