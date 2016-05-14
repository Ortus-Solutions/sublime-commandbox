# Sublime Commandbox

A plugin to run your [Commandbox](https://www.ortussolutions.com/products/commandbox) tasks from within Sublime plus some handy [snippets](#snippets) too.

## Quickstart

1. Install Via [Package Control](https://packagecontrol.io) `Commandbox`

## Installation

### via PackageControl
If you have [PackageControl](http://wbond.net/sublime_packages/package_control) installed, you can use it to install the package.

Just type `cmd-shift-p`/`ctrl-shift-p` to bring up the command pallete and pick `Package Control: Install Package` from the dropdown, search and select the package there and you're all set.

### Manually

You can clone the repo in your `/Packages` (*Preferences -> Browse Packages...*) folder and start using/hacking it.
    
    cd ~/path/to/Packages
    git clone git://github.com/Ortus-Solutions/sublime-commandbox.git Commandbox

### Troubleshooting

If you are having trouble running the plugin in **Mac OSX** it's possible that your path isn't being reported by your shell. In which case give the plugin [SublimeFixMacPath](https://github.com/int3h/SublimeFixMacPath) a try. It may resolve our issue.

If you still can't get it to run properly, first make sure your Commandbox tasks run from a terminal (i.e. outside of sublime) and if so then submit an [issue](https://github.com/Ortus-Solutions/sublime-commandbox/issues).

## Usage

### Available Commands

Sublime Commandbox supports the following commands accessible from `Tools -> Command Palette` by typing in "Commandbox". They are also accesible from menus as indicated below the table. `Default.sublime-commands` also lists them.

|     Command       |  From Command Palette | From Menu                 |
|:-----------------:|:---------------------:|:------------------------:|
| [box](#running-a-box-task)                | Commandbox or Commandbox (silent)     | List Tasks to Run |  

* The first five commands are available via `Tools -> Commandbox` in the main menu and in `Commandbox` in the sidebar context menu.
* The the remaining commands are available via `View -> Commandbox` in the main menu.


### Running a Commandbox Task
To run a task, first choose `Commandbox` from the command pallete or `List Tasks to Run` from the menu, the package will search for your tasks in the open folder/project and create a cache (`.sublime-commandbox.cache`) in the root. The first run will be slow as the cache builds but then the cache will speed up future access. You can use the [`box_delete_cache`](#deleting-the-cache) command to rebuild the cache if you are not seeing your newly added Commandbox Tasks or some have gone missing.

The plugin will then display all the Commandbox tasks in a list. Selecting one will run that task. To show the task's standard output the plugin uses a panel or a new tab (depends on your [settings](#settings)). After a first task has been run you can use the hide and show panel commands as desired. (see table above) 

If you want to run the normal `Commandbox` command without standard output to the panel use instead `Commandbox (silent)`. 

#### Arbitrary task

When running an arbitrary task you need to choose `Commandbox: Run arbitrary task` from the command pallete or `Run arbitrary task` from the menu. The package will then prompt an input panel where you can write what you want to add as a sufix to `box`.

### Customized Task Access

Out of the box Sublime Commandbox has a menu item `Run Default Task` under `Tools -> Commandbox` that will run your `default` Commandbox task. Most Commandbox users have a default task defined (like running their development tasks).

If you want to run other of your tasks from a menu item or [keyboard shortcut](#shortcut-keys) you can customize both.  

For example to add a menu item in the tools menu for a `sass` task do this. In your sublime user directory add following json in the `Main.sublime-menu` file (create one if you don't have one).

```json
{
    "id": "tools",
    "children": [
         { "caption": "Run Sass Task", "command": "box", "args": { "task_name": "sass" } }
     ]
}
```

_Note_: You can run any command silently by adding `"silent": true` to the `args`.

or you also can use a [keyboard shortcut](#shortcut-keys) to do the same. Edit `Preferences -> Key Bindings - User` to access the user key bindings file to which add this line:

````json
{ "keys": ["KEYS"], "command": "box", "args": { "task_name": "sass" } }
````

For more detailed information on [shortcut keys](#shortcut-keys) and [binding specific tasks](#bind-specific-tasks) below.

### Killing Tasks
To kill running tasks like `watch` you can pick the command `Commandbox: Kill running tasks`. 

**Windows**

If you're running Windows, the package will use [taskkill](http://technet.microsoft.com/en-us/library/cc725602.aspx) so every child process is correctly terminated. If the executable isn't on your system, you'll need to add it for this command to work correctly.

###  Show or Hide the Panel
`Commandbox: Show Panel` shows the closed output panel (just the panel, it won't re-open the tab if you're using the `results_in_new_tab` [setting](#settings)). Alternatively typing `<esc>` will also close/hide an open panel.

### Listing Commandbox Plugins
Running `Commandbox: List plugins` from the command palette will display all box plugins available on a searcheable list. Picking one will open its github repo on your default browser.

### Deleting The Cache
Running `Commandbox: Delete cache` will delete the `.sublime-commandbox.cache` file for you, forcing a re-parse of the `boxjson.js`.

### Quitting Sublime Killing Running Commandbox Tasks
This command will close Sublime Text, but first it'll kill any running tasks. It's the same as running `Commandbox: Kill running tasks` and immediately exiting the editor. If error occurs killing the tasks or no running tasks are found, the editor will close anyways.

You can select `Commandbox: Exit editor killing running tasks` from the command palette or create a [keybinding](#shortcut-keys) like this:

````
{ "keys": ["KEYS"], "command": "box_exit" }
````

You can bind it to `alt+f4` or `super+q` so you don't have to remember it. Sadly it **won't run** if you close the editor using the close button (**x**).



## Snippets

#### varbox
```
var box = require('box-name');
```

#### pipe
```
pipe(name('file'))
```

#### boxs - [Docs](https://github.com/boxjs/box/blob/master/docs/API.md#boxsrcglobs-options)
```
box.src('scriptFiles')
  .pipe(name('file'))
```

#### boxt - [Docs](https://github.com/boxjs/box/blob/master/docs/API.md#boxtaskname-deps-fn)
```
box.task('name',['tasks'], function() {
    // content
});
```

#### boxd - [Docs](https://github.com/boxjs/box/blob/master/docs/API.md#boxdestpath)
```
.pipe(box.dest('folder'));
```

#### boxw - [Docs](https://github.com/boxjs/box/blob/master/docs/API.md#boxwatchglob-opts-tasks)
```
box.watch('file', ['tasks']);
```

#### boxwcb - [Docs](https://github.com/boxjs/box/blob/master/docs/API.md#boxwatchglob-opts-cb)
```
box.watch('file', function(event) {
  console.log(' File '+event.path+' was '+event.type+', running tasks...');
});
```

## Settings

The file `Commandbox.sublime-settings` is used for configuration, you can change your user settings in `Preferences -> Package Settings -> Commandbox -> Settings - User`.

The defaults are:

````json
{
    "exec_args": {},
    "boxjson_paths": [],
    "results_in_new_tab": false,
    "results_autoclose_timeout_in_milliseconds": 0,
    "show_silent_errors": true,
    "log_errors": true,
    "syntax": "Packages/Commandbox/syntax/CommandboxResults.tmLanguage",
    "nonblocking": true,
    "flags": {},
    "check_for_boxjson": false,
    "tasks_on_save": {},
    "silent_tasks_on_save": {}
}
````

#### exec_args

You may override your `PATH` environment variable as follows (from [sublime-grunt](https://github.com/tvooo/sublime-grunt)):

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

#### boxjson_paths

Additional paths to search the boxjson in, by default only the root of each project folder is used.
Example: `["src", "nested/folder"]`

#### results_autoclose_timeout_in_milliseconds

Defines the delay used to autoclose the panel or tab that holds the box results.
If false (or 0) it will remain open, so if what you want is to keep it closed check the [`silent`](#running-a-box-task) command.

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

#### flags

This seting lets you define custom flags for your box commands. The key is the name of the task and the value is the string containing the flags.

For example if you have to run `build` with the `--watch` flag, like this `box build --watch` you'll do:

````json
{
    "flags": {
        "build": "--watch"
    }
}
````

If you want to add a flag to a task just for a project, you can try [binding a specific task](#bind-specific-tasks).

#### check_for_boxjson

If `false` the package will run even if no `boxjson.js` is found on the root folders currently open.

So for example, if you have *5* root folders on your Sublime sidebar and only *3* of them have a `boxjson`, when you run `Sublime Commandbox` with `check_for_boxjson: true` it'll only show the *3* that have a `boxjson.js`, but if you set `check_for_boxjson` to false, it'll list _all_ *5* folders.

You might want to set it to false if you're using the `--boxjson` flag, or if you want to leave the error reporting to box.

#### tasks_on_save

Allows you to run task(s) when you save a file. The key is the name of the task and the value is the string or array of glob pattern.

The base folder for glob pattern is the first folder in you project. So, if you have multiple folder, the glob pattern will only match on the first folder.

````javascript
{
    "tasks_on_save": {
        // Run browserify task when you save javasript file
        "browserify": "*.js",
        // Run sass task when you save sass file under "sass" folder
        "sass": "sass/*.scss",
        // Array of glob pattern
        "other": ["*.ext1", "*.ext2"]
    }
}
````

#### silent_tasks_on_save

Works the same way as [tasks_on_save](https://github.com/Ortus-Solutions/sublime-commandbox#tasks_on_save) but it runs the tasks on `silent` mode (using `Commandbox (silent)`).

### Per project settings

If you want to have a per project settings, you first need to create a [project](https://www.sublimetext.com/docs/2/projects.html) going to `Project -> Save Project As` and then edit your project file (you can use `Project -> Edit Project`).
In there you can override Commandbox settings like so:


````javascript
{
    "settings": {
        "results_in_new_tab": true
    },

    // Or, Sublime Text 3 only:
    "Commandbox": {
        "check_for_boxjson": false
    }
}
````

The package will search first on `"settings": {}`, then on `"Commandbox": {}` (ST3 only) and lastly on the `Commandbox.sublime-settings` file.

Keep in mind that the only *caveat* is that if you want to override the `syntax` key, you'll need to use `syntax_override` as key.

For a visual example go to [this comment on issue 53](https://github.com/Ortus-Solutions/sublime-commandbox/issues/53#issuecomment-153012155)


## Shortcut Keys

This package doesn't bind any command to a keyboard shortcut, but you can add it like this:

````json
[
    { "keys": ["KEYS"], "command": "box" },

    { "keys": ["KEYS"], "command": "box_arbitrary" },

    { "keys": ["KEYS"], "command": "box_exit" },

    { "keys": ["KEYS"], "command": "box_show_panel" },

    { "keys": ["KEYS"], "command": "box_hide_panel" },

    { "keys": ["KEYS"], "command": "box_namespaces" },

    { "keys": ["KEYS"], "command": "box_exit" }
]
````


#### Bind specific tasks

You can use a shortcut for running a specific task like this:

````json
{ "keys": ["KEYS"], "command": "box", "args": { "task_name": "watch" } }
````

and if you want to run it in [`silent`](#running-a-box-task) mode, you can add `"silent"` to the `args`

````json
{ "keys": ["KEYS"], "command": "box", "args": { "task_name": "watch", "silent": true } }
````

Lastly, you can add a flag to the command using `task_flag`. This option will override the any [flag](#flags) defined on the settings file.  

````json
{ "keys": ["KEYS"], "command": "box", "args": { "task_name": "build", "task_flag": "--watch" } }
````

_Note_: You can run commands like `box -v` if you set `task_name` to `""` (empty string) with a flag.

##Acknowledgments

This package is a merge between [Commandbox Snippets](https://github.com/filipelinhares/box-sublime-snippets) from [@filipelinhares](https://github.com/filipelinhares) and [Commandbox](https://github.com/Ortus-Solutions/sublime-commandbox) from [NicoSantangelo](https://github.com/NicoSantangelo) (this last one, inspired by the awesome [sublime-grunt](https://github.com/tvooo/sublime-grunt)).

Thanks to [@dkebler](https://github.com/dkebler) for re-writing the README.
