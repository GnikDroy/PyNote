<p align="center">
<h1 align="center"> Py-notepad </h1>

<h3 align="center">A simple cross-platform text-editor written in python.</h3>

<img src="https://raw.githubusercontent.com/GnikDroy/py-notepad/master/screenshots/screenshot.png">
</p>

**This project was for fun so, is not maintained. I work on it sometime as recreation. We would need to rewrite this in something modern if we wish to continue.**

## Features

### Syntax Highlighting

#### Supported Languages
- C
- C++
- Java
- Python
- Go
- Haskell
- Javascript

It's quite easy to extend. Let's take a look at how you can add support for your custom language.
All language support is kept in the file **"keywords.ini"**

The following lines add support for python.
```
Python,py
False,None,True,and,as,assert,....
```

So the general format for a language looks like

```
[LanguageName],[LanguageExtension]
[Keyword],[Keyword2]......
```

Notice that everything is delimited by comma.
And after each language support is a extra new line. 
(Just because it was easier to read for me)
You can use those lines for commenting.

Therefore, to add multiple languages you can use the following format:

```
Language Name,Language extension
keyword,keyword2......

Language Name,Language extension
keyword,keyword2......

```

### Line Numbers
You can toggle them on/off. They are also fully compatible with word wrap
and take very low resource.

### Custom build scripts
The custom build scripts are just a bash script supplied with a filename.
Yes, it is rather crude but we have to make do with what little time we have.

Let's take a look at one of the build scripts for python.

```
#!/usr/bin/env bash

python -m py_compile $1
echo
echo _________________________
echo Press any key to continue
read -n1
```

As you can see, $1 represents the filename.
That is the only thing you are provided.

The editor then uses the gnome-terminal to run the commands.
Therefore, you must modify some things to make it run properly in windows.
Since windows doesn't have any terminal/terminal emulators, you should create a batch-file instead.

You can change them to your own terminal emulator.
Also you can change the shell to anything you like: sh,bash ...etc

Notice that there are three variants of the scripts:
- pybuild.sh
- pycompile.sh
- pyexecute.sh

Also notice that the language is denoted by it's extension.

So for C#, the files would be: csbuild.sh, csexecute.sh and cscompile.sh
It is not neccessary to use all of them. 

** It is neccessary to register the language in the keyword file before creating build scripts for it. **
 

### All Major Keyboard Bindings
Honestly, tkinter text boxes support a lot of keybindings by default.
I just added some common bindings to make using it more productive.

It can handle fairly large files unlike the windows version. If something slows down, then it is due to the crude custom syntax highlighting implemented by regex.
You can disable it to make the program faster.

If you are feeling adventurous make your own highlighter and issue a pull request.
You might me thinking what the `AlternativeHighlighter.py` does.
It is left as an exercise to you.
Even though this project is not maintained, I will add stuff if you issue a request. 
 
## How to Run

**Use Python 2**

If you have Python installed then you can simply run `python Editor.py`


## Requirements
- tkinter
Everything else should be in the standard Python package.

