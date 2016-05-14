# Sublime Commandbox

A plugin to run [Commandbox](https://www.ortussolutions.com/products/commandbox) Commands, including server management and scaffolding, from within Commandbox.

## Quickstart

1. Install Via [Package Control](https://packagecontrol.io) `Commandbox`

## Installation

### via PackageControl
If you have [PackageControl](http://wbond.net/sublime_packages/package_control) installed, you can use it to install the package.

Just type `cmd-shift-p`/`ctrl-shift-p` to bring up the command pallete and pick `Package Control: Install Package` from the dropdown, search and select the `CommandBox` package there and you're all set.

### Manually

You can clone the repo in your `/Packages` (*Preferences -> Browse Packages...*) folder and start using/hacking it.
    
    cd ~/path/to/Packages
    git clone git://github.com/Ortus-Solutions/sublime-commandbox.git Commandbox

### Troubleshooting

If you are having trouble running the plugin in **Mac OSX** it's possible that your path isn't being reported by your shell. In which case give the plugin [SublimeFixMacPath](https://github.com/int3h/SublimeFixMacPath) a try. It may resolve our issue.

If you still can't get it to run properly, first make sure your Commandbox tasks run from a terminal (i.e. outside of sublime) and if so then submit an [issue](https://github.com/Ortus-Solutions/sublime-commandbox/issues).

## Usage

### Running a Commandbox Command

You may select pre-configured commands from `Menu -> Commandbox`, including the ability enter a custom command.

#### Keyboard Shortcuts:

* `Ctrl+Shift+B` - Run Commandbox Command: A prompt input will open for you to enter your command
* `Ctrl+Shift+T` - Start the Embedded Server: Your Commandbox `cwd` is always the root of your Sublime Project so any `box.json` configuration will be honored
* `Ctrl+Shift+P` - Stop the Embedded Server
* `Alt+P` - Show the Commandbox Output Panel ( also available in the `View -> Commandbox` menu )
* `Alt+[Command|Windows]+P` - Hide the Commandbox Output Panel ( also available in the `View -> Commandbox` menu )

## Settings

The file `Commandbox.sublime-settings` is used for configuration, you can change your user settings in `Preferences -> Package Settings -> Commandbox -> Settings - User`.

The defaults are:

````json
{
    "exec_args": {},
    "results_in_new_tab": false,
    "results_autoclose_timeout_in_milliseconds": 0,
    "show_silent_errors": true,
    "log_errors": true,
    "syntax": "Packages/Commandbox/syntax/CommandboxResults.tmLanguage",
    "nonblocking": true,
    "check_for_boxjson": true,
}
````

#### exec_args

You may override your `PATH` environment variable as follows:

````json
{
    "exec_args": {
        "path": "/bin:/usr/bin:/usr/local/bin"
    }
}
````

##### box installed locally

If box is installed locally in the project, you have to specify the path to the box executable. Threfore, adjust the path to `/bin:/usr/bin:/usr/local/bin:node_modules/.bin`

#### results_in_new_tab

If set to `true`, a new tab will be used instead of a panel to output the results.

#### results_autoclose_timeout_in_milliseconds

Defines the delay used to autoclose the panel or tab that holds the Commandbox results.

#### show_silent_errors

If true it will open the output panel when running [`Commandbox (silent)`](#running-a-box-task) only if the task failed

#### log_erros

Toggles the creation of `sublime-commandbox.log` if any error occurs.

#### syntax

Syntax file for highlighting the box results. You can pick it from from the command panel as `Set Syntax: Commandbox results`.

Set the setting to `false` if you don't want any colors (you may need to restart Sublime if you're removing the syntax).

#### nonblocking

When enabled, the package will read the streams from the task process using two threads, one for `stdout` and another for `stderr`. This allows all the output to be piped to Sublime live without having to wait for the task to finish.

If set to `false`, it will read first from `stdout` and then from `stderr`.

#### Bind Your Own Keyboard Shortcuts

You can use a shortcut for running a specific task like this:

````json
{ "keys": ["KEYS"], "command": "commandbox", "args": { "task_name": "watch" } }
````

#### LICENSE

Sublime-CommandBox is open source and bound to the LGPL v3 GNU LESSER GENERAL PUBLIC LICENSE Copyright & TradeMark since 2014, Ortus Solutions, Corp

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.