# Docc -- A simple MarkDown documentation generator

### Installation

Clone this repo and run `sh install.sh` to install. You will be prompted for a root password to install the dependencies, docc, and the base template.

### Usage

Once you've installed docc, run it with the `docc` command. This will read all the markdown files in your current directory and any subdirectories and compile them, and place them in another dir. By default files will be saved under `dist/files.md`. 


### Configuration

If you provide a `docc.toml` file in the same directory you are running the `docc` command from, it will use the settings from that file for configuration. Here is an example `docc.toml` file:

```toml
title = "my program's documentation" # The title to be used in the compiled documentation
out = "docs" # the output directory
ignore = [ # the files to ignore while compiling
  "readme.md",
  "src/athing.md"
]
template = "docs/template.html" # the location of the template to render to
```
Leave any of these blank to use the defaults.
