+++
title = "My auto-reload setup for writing LATEX documents in VIM"
date = Date(2021, 01, 17)
rss = "autolatex"
tags = ["productivity"]
descr = "Zathura + latexmk -> :). Latest update: 17th January 2021."
+++

# {{ title }}

\toc

## (Update) January 17th 2021
It's a new year, and I've been using a new workflow for writing my LATEX
documents in Vim.  One frustratation I had with my previous set up (see below)
was the complicated nature of having automatic reloading using Firefox as my PDF
viewer. Also, sometimes I don't want to open such a power hungry app just to
view a PDF. So I now use [Zathura](https://pwmt.org/projects/zathura/), a
minmial PDF viewer with customizable keyboard shortcuts (e.x. Vim key-bindings
for moving around) that can be continously updated by the compiler ``latexmk``,

```bash
$ latexmk -pdf -pvc report.tex
```

The `-pvc` option allows for continuous previewing, which compiles the tex file
at each write. As you could guess, `-pdf` option compiles the file to
`report.pdf`. With the continous previewing, we want to keep `latexmk` command
running. It's useful to keep it in a separate terminal (don't push it to the
background) as it will show us any warnings and compilation errors. When these
happen, we can acknowledge the error with `Ctrl-D`, which tells `latexmk` to
try compile the next file write. 

We can open the PDF file via the terminal with,

```bash
$ zathura report.pdf --fork
```

The fork option allows us to close terminal. Alternatively, we can set Zathura
to our default PDF viewer in our `~/.bashrc` via `$ export READER=zathura`.

### REALLY setting your default viewer
However, not all programs look at your environment variables to open files. A
more widely used option is with the
[`xdg-open`](https://man.archlinux.org/man/xdg-open.1) command, which your
computer will call by default when openning a file. There have been written many
versions of this command. I've found
[mimi](https://github.com/march-linux/mimi), which seems to have most easily
configurable `xdg-open` "mime-types". Replace your default `xdg-open` with the one in
the mimi repository (or add `xdg-open` to another fold with greater precedence
in your `$PATH` variable). You can then make Zathura, or any other program, you
default PDF viewer with the line `application/pdf: zathura` in the
mimi configuration file, `~/.config/mimi/mime.conf`.

### Zathura options
Zathura looks for a configuration file called `~/.config/zathura/zathurarc`.
I set some options like making zooming in and out easier and more:
```plaintext
map K zoom in
map J zoom out
map u scroll half-up
map d scroll half-down
map r reload
map R rotate
set selection-clipboard clipboard
```
Many many more options are available and can be found in the
[`zathurarc`](http://manpages.ubuntu.com/manpages/trusty/man5/zathurarc.5.html) man
page.

## January 3rd 2020
I'm so happy with my current LATEX workflow that I want to share it. It is actually 
quite a niche problem that it's solving because it's born out of using VIM as my 
editor (a command-line editor) and Firefox as my PDF viewer. I enjoy VIM as its keyboard 
shortcuts allow me to write without being slowed down by using a mouse. Firefox is 
my PDF viewer of choice because 1. I always have it open anyway, and 2. It has a clean UI 
with features I like such as a table of contents and printing. 

### My (Old) Setup:
- Windowing System: X11 (this becomes important for the reload script)
- Editor: VIM
- PDF Viewer: Firefox
- Compilation: **MANUAL**, using ``latexmk``

Manually compiling my LATEX document to preview my work involves to following 7 lines 
of keyboard strokes. It may not seem like a lot but it quickly gets annoying. 

```plaintext
:w                      # write file in VIM
Ctrl-Z                  # stop VIM and put to background
latexmk -pdf report.tex # compile to pdf
Alt-Tab                 # swtich to Firefox
Ctrl-R                  # reload tab
Alt-Tab                 # switch to Terminal
fg                      # bring VIM to foreground, continue with life
```

I knew there had to be a better way. My goal was to find a method of having my 
computer listen for file changes in my ``.tex`` file and automatically compile to PDF 
and reload the viewer. 

### Automatic Tab-Reload in Firefox using XDOTOOL:
Sadly Firefox doesn't currently support automatic reload of a tab based on local 
file change (I believe it used to have a plugin for this, however, it was removed 
due to security risks). A workaround for this is using 
``xdotool - a command line X11 automation tool``. For those of us on UNIX-based operating 
systems (I believe almost all of which use X11, or some variant which allows ``xdotool`` 
to work), this lets us interact with our windows 
from the command line. That means we can essentially automate our ``Ctrl-R`` and ``Alt-Tab`` 
key-strokes from before. After some skimming of the man page and stackoverflow I arrived at 
the following reload script that gets the job done.

My ``reload`` bash script:
```bash
#!/bin/sh
CURRENT_WID=$(xdotool getactivewindow)                     
WID=$(xdotool search --name "report.pdf - Mozilla Firefox")
xdotool windowactivate --sync $WID                         
xdotool key F5                                             
xdotool windowactivate $CURRENT_WID                        
```
In the first two lines of the above script we get the names of the current window 
(our terminal emulator) and the Firefox PDF window. We then switch focus to 
the PDF window with ``windowactivate`` and use the ``--sync`` argument to ensure 
we only run the next line after we're confirmed to be focused on the window. 
We then use ``xdotool`` to hit the ``F5`` key, equivalent to hitting ``Ctrl-R``. 
Finally we return focus to the command line.

Running the script via ``./reload`` will reload the current tab on the Firefox 
window that is viewing the file ``report.pdf``. Change the filename used in the script 
to your own accordingly. Don't forget to add execute permissions to the script by running 
``chmod +x reload``. All we have left to do is figure out how to run this script 
whenever our tex file is written to.

### Listening for File-Changes with ``entr`` and My New Setup:

We can then use the command line tool [``entr - run arbitrary commands when a 
file changes``](https://eradman.com/entrproject/) 
to continuously listen for any file changes to ``report.tex`` and run our ``reload`` script. 
The following line in bash does the trick:

```bash
$ ls report.tex | entr -ps 'latexmk -pdf report.tex; ./reload'
```

``ls`` lists information about ``report.tex`` and is piped into ``entr`` 
which listens for changes. The ``-p`` option tells ``entr`` to wait 
until the first change is noticed. The ``-s`` option allows us to 
give some shell commands in single-quotes, where we've opted to 
compile our tex file to pdf with ``latexmk`` and then run our ``reload`` script.
You can keep this command in another terminal window or run it in the background 
of your current one. I keep it running in the foreground of another TMUX pane  
to the side of my VIM pane so that I can see any error messages if 
they occur.

My new setup now consists of simply writing the above bash one-liner 
at the start of each editing session, opening my draft PDF in Firefox with 
``firefox report.pdf``, and then saving my work in VIM with ``:w`` whenever I want 
to update my preview. The compilation and PDF reload now happens automatically whenever 
I save my tex file!

### Future Work and Remarks:
- The ``reload`` script relies on the current tab being the PDF tab. 
  A better implementation would reload the tab if it was in the background.
- Every time I start editing a new project I have to *manually* type in the 
  little ``ls | entr`` bash one-liner. I should really put this into a script that 
  just takes in a filename.
- Note that the ``entr`` documentation mentions the use of their own 
  ``reload-browser`` script. In testing it myself I found that it occasionally fails 
  due to the lack of the ``--sync`` argument in the ``xdotool windowactivate`` command. 
  It's also nice to write your own scripts so that you really understand what's going on!


