"""
hosts.py contains classes for sending python commands to various Autodesk
clients.
"""
import abc
from enum import Enum
import socket
import telnetlib
import time


class Hosts(Enum):
    """ Host enum values """
    UNKNOWN = 0
    MAYA = 1
    MOTIONBUILDER = 2


class AbstractHost(object):
    """ Abstract base class for host object """
    __metaclass__ = abc.ABCMeta

    def __init__(self, host, port):
        self._host = host
        self._port = port

    def send(self, commands):
        """ Send commands to host

        Args:
            commands (list(str)): Commands to send

        Returns:
            (float): The time to execute the commands in seconds
        """

        start_time = time.time()

        # Send the commands
        self._send_impl(commands)

        # Calculate how long it takes to execute the commands
        end_time = time.time()
        return float(end_time - start_time)


    @abc.abstractmethod
    def _send_impl(self, commands):
        """ Sending commands to be implemented by concrete host classes

        Args:
            commands (list(str)): Commands to send
        """
        pass


class NullHost(AbstractHost):
    """ Host class for null pattern """
    _host_type = Hosts.UNKNOWN

    def _send_impl(self, commands):
        raise RuntimeError(
            "Unknown host is not defined. Unable to send commands")


class MayaHost(AbstractHost):
    """ Host class for dealing with Maya """
    _host_type = Hosts.MAYA

    @staticmethod
    def _format_command(command):
        """ Format the command to be sent to Maya

        Args:
            command (str): The command to format

        Returns:
            str:
        """
        command = command.replace('"', '\\"')
        command = "python (\"{}\");".format(command)
        return command.encode("utf-8")

    def _send_impl(self, commands):

        # Create connection to the command port
        try:
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection.connect((self._host, self._port))
        except socket.error as err:
            raise RuntimeError("Failed to connect to Maya: {}".format(err))

        # Set timeout for the script to run in Maya
        connection.settimeout(30.0)

        # Send commands
        try:
            for command in commands:
                connection.send(self._format_command(command))
                connection.recv(4096)
        except socket.error:
            raise RuntimeError(
                "Failed to send commands to Maya: {}".format(commands))
        finally:
            # Shutdown the socket
            connection.shutdown(socket.SHUT_WR)
            connection.close()


class MobuHost(AbstractHost):
    """ Host class for dealing with Motionbuilder """
    _host_type = Hosts.MOTIONBUILDER

    @staticmethod
    def _format_command(command):
        return "{}\n".format(command)

    def _send_impl(self, commands):

        # Create connection to telnet server
        try:
            connection = telnetlib.Telnet(self._host, self._port)
        except socket.error as err:
            raise RuntimeError(
                "Failed to connect to Motionbuilder: {}".format(err))

        # Read until we get the ">>>" from the python console
        connection.read_until(">>>")

        # Send commands
        try:
            for command in commands:
                connection.write(self._format_command(command))
                connection.read_until(">>>")
        except EOFError:
            raise RuntimeError(
                "Connection from Motionbuilder was closed before could finish")
        except socket.error:
            raise RuntimeError(
                "Failed to send commands to Motionbuilder: {}".format(
                    commands))
        finally:
            # Close the connection
            connection.close()


def host_factory(host):
    """ Get the appropriate host class """
    return {
        Hosts.MAYA: MayaHost,
        Hosts.MOTIONBUILDER: MobuHost,
    }.get(host, NullHost)
