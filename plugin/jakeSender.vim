"==============================================================================
" File:  jakeSender.vim
" Description: vim plugin that allows you to send buffers or lines of code to
"              Maya or Motionbuilder
" Author: Lex French <LexFrench at gmail dot com>
" Maintainer: Lex French <LexFrench at gmail dot com>
" Version: 0.0.1
" Last Change: Sun Sep 23 21:04:12 +08 2018
" License: Copyright (C) 2018 Alexander French
"
"          This program is free software: you can redistribute it and/or modify
"          it under the terms of the GNU General Public License as published by
"          the Free Software Foundation, either version 3 of the License, or
"          (at your option) any later version.
"
"          This program is distributed in the hope that it will be useful,
"          but WITHOUT ANY WARRANTY; without even the implied warranty of
"          MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
"          GNU General Public License for more details.
"
"          You should have received a copy of the GNU General Public License
"          along with this program.  If not, see <https://www.gnu.org/licenses/>
"
"==============================================================================

" Set Configuration defaults

" Host's address to send commands (This should be localhost in most cases)
if !exists('g:jakeSenderHost')
    let g:jakeSenderHost = 'localhost'
endif

" The port to send Maya commands to
if !exists('g:jakeSenderMayaPort')
    let g:jakeSenderMayaPort = 8722
endif

" Telnet port for Motionbuilder's python server
if !exists('g:jakeSenderMobuPort')
    let g:jakeSenderMobuPort = 4242
endif

" Root directory of the plugin (DO NOT TOUCH!)
if !exists('g:jakeSenderRootDir')
    let s:jakeSenderRootDir = fnamemodify(resolve(expand('<sfile>:p')), ':h')
endif

" Key Mappings

" Send buffer to Maya hotkeys
nnoremap <leader>m :SendBufferToMaya<cr>
vnoremap <leader>m :<C-U>SendBufferToMaya<cr>

" Send buffer to Mobu hotkeys
nnoremap <leader>x :SendBufferToMobu<cr>
vnoremap <leader>x :<C-U>SendBufferToMobu<cr>

" Send current line to Maya hotkeys
nnoremap <leader>lm :SendLineToMaya<cr>
vnoremap <leader>lm :<C-U>SendLineToMaya<cr>

" Send current line to Mobu hotkeys
nnoremap <leader>lx :SendLineToMobu<cr>
vnoremap <leader>lx :<C-U>SendLineToMobu<cr>

" Send Selection to Maya hotkeys
nnoremap <leader>sm :SendSelectionToMaya<cr>
vnoremap <leader>sm :<C-U>SendSelectionToMaya<cr>

" Send Selection to Mobu hotkeys
nnoremap <leader>sx :SendSelectionToMobu<cr>
vnoremap <leader>sx :<C-U>SendSelectionToMobu<cr>

" Let's check that we have python support (for people that didn't RTFM)
if !has ('python')
    echoerr "vim-JakeSender requires Vim compiled with Python support."
    finish
endif
"
" Python code (This is where the magic is)

python << EOF

import sys
from os.path import normpath, join
import vim

# Get the python code dir
plugin_root_dir = vim.eval('s:jakeSenderRootDir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))

# Add dir to path
sys.path.insert(0, python_root_dir)

# Run our plugin's actual code
import jake

# Setup public methods
send_current_line_to_maya = jake.send_current_line_to_maya
send_current_line_to_mobu = jake.send_current_line_to_mobu

send_buffer_to_maya = jake.send_buffer_to_maya
send_buffer_to_mobu = jake.send_buffer_to_mobu

send_selection_to_maya = jake.send_selection_to_maya
send_selection_to_mobu = jake.send_selection_to_mobu

EOF

" Commands

command! -nargs=0 SendLineToMaya :py send_current_line_to_maya()
command! -nargs=0 SendLineToMobu :py send_current_line_to_mobu()
command! -nargs=0 SendBufferToMaya :py send_buffer_to_maya()
command! -nargs=0 SendBufferToMobu :py send_buffer_to_mobu()
command! -nargs=0 SendSelectionToMaya :py send_selection_to_maya()
command! -nargs=0 SendSelectionToMobu :py send_selection_to_mobu()
