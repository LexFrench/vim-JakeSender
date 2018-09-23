# vim-JakeSender
[![GPL Licence](https://badges.frapsoft.com/os/gpl/gpl.png?v=103)](https://opensource.org/licenses/GPL-3.0/) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/20393bee21b04aacb525b0384d5ebfcb)](https://www.codacy.com/app/lexfrench/vim-JakeSender?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LexFrench/vim-JakeSender&amp;utm_campaign=Badge_Grade) [![Maintainability](https://api.codeclimate.com/v1/badges/9f6c46fa47690a04fb59/maintainability)](https://codeclimate.com/github/LexFrench/vim-JakeSender/maintainability) [![CodeFactor](https://www.codefactor.io/repository/github/lexfrench/vim-jakesender/badge)](https://www.codefactor.io/repository/github/lexfrench/vim-jakesender)

<p align="center">
  <img style="float: right; height: 200px;" src="assets/jake.png" alt="Vim-JakeSender logo"/>
</p>

JakeSender is a basic vim plugin for sending python code from the current vim
buffer (or visual selection) to Autodesk's Maya or Autodesk's Motionbuilder

Jake is a good boy (sic) that will hide your commands, like a bone, in a
special safe place ($TEMPDIR) and then like Lassie, go tell Maya or
Motionbuilder where to find the file and to execute the content.

## Installation

### Via Plugin Manager (USE ONE!)

#### [Vim-Plug](https://github.com/junegunn/vim-plug)

1. Add `Plug 'lexfrench/vim-jakesender'` to your vimerc file
2. Reload your vimrc or restart vim
3. `:PlugInstall`

#### [Vundle](https://github.com/VundleVim/Vundle.vim) or similar

1. Add `Plugin 'lexfrench/vim-jakesender'` to your vimrc file
2. Reload your vimrc or restart
3. Run `:BundleInstall`

#### [NeoBundle](https://github.com/Shougo/neobundle.vim)

1. Add `NeoBundle 'lexfrench/vim-jakesender'` to your vimrc file
2. Reload your vimrc or restart
3. Run `:NeoUpdate`

#### [Pathogen](https://github.com/tpope/vim-pathogen)

```sh
cd ~/.vim/bundle
git clone https://github.com/lexfrench/vim-jakesender.git
```
### Manual Installation

#### Unix

(For Neovim, change `~/.vim/` to `~/.config/nvim/`.)

```sh
curl -fLo ~/.vim/plugin/jakeSender.vim --create-dirs \
  https://raw.githubusercontent.com/lexfrench/vim-jakesender/master/plugin/jakeSender.vim
curl -fLo ~/.vim/doc/jakeSender.txt --create-dirs \
  https://raw.githubusercontent.com/lexfrench/vim-jakesender/master/doc/jakeSender.txt
```

### Maya Configuration

In order to send commands to Maya, you'll need to enable the command port on startup. This can be done by adding the following to your `userSetup.py` file in your Maya scripts folder.

1. Create a `userSetup.py` file if you don't already have one

```
touch ~/maya/scripts/userSetup.py
```

2. Add the following 
```python
import maya.cmds as cmds

cmds.commandPort(name=":8722", sourceType="mel", noreturn=False, echoOutput=False, bufferSize=4096)
```

### Motionbuilder Configuration

In order to send commands to Motionbuilder, you'll need to enable the python server in the Motionbuilder Preferences. [Check here.](http://bit.ly/MobuPythonPrefs)

## Usage

### Documentation

Please see the vim help system for full documentation of all options: `:help jakeSender`

### Commands

The following commands are available to send the buffer content to supported hosts (Maya and Motionbuilder):
  * `SendBufferToMaya` : Sends the current buffer OR visual selection to Maya's command port
  * `SendBufferToMobu` : Sends the current buffer OR visual selection to Motionbuilder's telnet server
  * `SendLineToMaya`   : Sends the current (single) line to Maya's command port
  * `SendLineToMobu`   : Sends the current (single) line to Motionbuilder's telnet server


### Basic Settings

```vim
" Host's address to send commands (This should be localhost or 127.0.0.1 in 99.99999% of the cases)
let g:jakeSenderHost="localhost"

" The port to send Maya commands to
let g:jakeSenderMayaPort=8722

" The telnet port for Motionbuilder's python server
let g:jakeSenderMobuPort=4242
```

### Default mappings

The following key mappings are provided by default:
  * `<leader>m` **[SendBufferToMaya]**
  * `<leader>x` **[SendBufferToMobu]**
  * `<leader>lm` **[SendLineToMaya]**
  * `<leader>lx` **[SendLineToMobu]**

## FAQ
**Q** Why did you write this plugin? Aren't there other plugins for sending commands to Maya? \
**A** Hi Carl, you don't mind if I call you Carl do you? So Carl, you're absolutely right, there are other plugins that send commands to Maya's command port. If you don't like mine, you should check out [Vimya](https://www.vim.org/scripts/script.php?script_id=2626). However, for the cases I found myself in, Vimya just didn't cut it. Specifically, I wanted to send commands to both Maya and Motionbuilder, since I use both at work quite frequently. Also, I've never written a vim plugin and this seemed like a good way to spend my Saturday. So to answer your question Carl, the main reason I created this package is because I GODDAMN WANTED TO! Sheesh Carl, you're so ungrateful!

**Q** Why do you call it JakeSender? \
**A** I'm glad you asked Carl! You see, at my office (where I'm going to be using this) we have an awesome office dog name Jake! And much like this tool, Jake makes my life a little better at work. But Carl, wouldn't you know it, there already is a vim-jake plugin on github. So I decided to go with JakeSender, since the script sends stuff... Get it Carl?

**Q** Can you port this plugin to Atom, Visual Studio Code, etc.? \
**A** Carl, do you see me using Atom, Visual Studio Code or other inferior editors at work? Why would I waste my time writing plugins for those editors when I'm perfectly happy in vim/neovim land?

**Q** Why do you keep calling me Carl? \
**A** Stop asking dumb questions Carl.

