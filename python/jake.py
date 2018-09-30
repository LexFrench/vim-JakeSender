"""
Jake allows you to run the current vim buffer (or portions of it) in various
Autodesk hosts.

Author: Lex French
Date Created: 9/22/2018
Python Version: 2.7
License: GPL3
"""

import os
import tempfile

import vim

from hosts import Hosts, host_factory
from vim_utils import BufferRange


# Get the globals from the vim config settings
HOST = vim.eval("g:jakeSenderHost")
MAYA_PORT = int(vim.eval("g:jakeSenderMayaPort"))
MOBU_PORT = int(vim.eval("g:jakeSenderMobuPort"))

# -----------------------------------------------------------------------------
# Generic functions for sending buffers or lines to host applications


def send_current_line_to_host(host_type, host, port):
    """ Send the current line to the host

    Args:
        host_type (Hosts.*): Enum value for which host you want to send to
        host (str): Host's server address
        port (int): Host's server port
    """
    commands = []

    # Get line and add it to commands list
    line = vim.current.line
    commands.append(line)

    # Send to appropriate host
    active_host = host_factory(host_type)(host, port)
    total_time = active_host.send(commands)

    # Let the user know how long it took
    vim.command('redraw | echo "Execution Time: {0:.3f}s"'.format(total_time))


def send_buffer_to_host(host_type, host, port):
    """ Send the current buffer to the host

    Args:
        host_type (Hosts.*): Enum value for which host you want to send to
        host (str): Host's server address
        port (int): Host's server port
    """
    commands = []

    # Get the current buffer and <> marks in vim
    buf = vim.current.buffer

    # Create a tempfile
    temp_file = tempfile.NamedTemporaryFile("w", delete=False)

    # Write out the buffer to the temp file
    for line in buf:
        temp_file.write("{}\n".format(line))

    # Close the file so the host can open it
    temp_file.close()

    # Add a command to execute our temp file
    commands.append("execfile('{}')".format(temp_file.name))

    # Send to appropriate host
    active_host = host_factory(host_type)(host, port)
    total_time = active_host.send(commands)

    # Let the user know how long it took
    vim.command('redraw | echo "Execution Time: {0:.3f}s"'.format(total_time))

    # Clean up the temp file
    if os.path.isfile(temp_file.name):
        os.remove(temp_file.name)


def send_selection_to_host(host_type, host, port):
    """ Send the current selection to the host

    Args:
        host_type (Hosts.*): Enum value for which host you want to send to
        host (str): Host's server address
        port (int): Host's server port
    """
    commands = []

    # Get the current buffer and <> marks in vim
    buf = vim.current.buffer
    start_line, start_col = buf.mark("<")
    end_line, end_col = buf.mark(">")

    # Create a tempfile
    temp_file = tempfile.NamedTemporaryFile("w", delete=False)

    if start_line == 0 or end_line == 0:
        vim.command('redraw | echoerr "No selection marks specified"')
        return
    else:
        # The user has selected some subsection of code they would like to send
        for line in BufferRange(start_line, end_line, start_col, end_col):
            temp_file.write("{}\n".format(line))

    # Close the file so the host can open it
    temp_file.close()

    # Add a command to execute our temp file
    commands.append("execfile('{}')".format(temp_file.name))

    # Send to appropriate host
    active_host = host_factory(host_type)(host, port)
    total_time = active_host.send(commands)

    # Let the user know how long it took
    vim.command('redraw | echo "Execution Time: {0:.3f}s"'.format(total_time))

    # Clear the vim marks
    vim.command("delmarks <")
    vim.command("delmarks >")

    # Clean up the temp file
    if os.path.isfile(temp_file.name):
        os.remove(temp_file.name)
# -----------------------------------------------------------------------------
# Functions for sending to Maya and Motionbuilder


def send_current_line_to_maya():
    """ Send the current line to Maya """
    send_current_line_to_host(Hosts.MAYA, HOST, MAYA_PORT)


def send_current_line_to_mobu():
    """ Send the current line to Mobu """
    send_current_line_to_host(Hosts.MOTIONBUILDER, HOST, MOBU_PORT)


def send_buffer_to_maya():
    """ Send the current buffer to Maya """
    send_buffer_to_host(Hosts.MAYA, HOST, MAYA_PORT)


def send_buffer_to_mobu():
    """ Send the current buffer to MOTIONBUILDER """
    send_buffer_to_host(Hosts.MOTIONBUILDER, HOST, MOBU_PORT)


def send_selection_to_maya():
    """ Send the current selection to Maya """
    send_selection_to_host(Hosts.MAYA, HOST, MAYA_PORT)


def send_selection_to_mobu():
    """ Send the current selection to Maya """
    send_selection_to_host(Hosts.MOTIONBUILDER, HOST, MOBU_PORT)
