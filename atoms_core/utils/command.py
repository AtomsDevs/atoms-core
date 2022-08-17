# command.py
#
# Copyright 2022 mirkobrombin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundationat version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
import os
import copy
import shutil
import logging
import subprocess
import contextlib
from typing import Union
from functools import lru_cache

from atoms_core.exceptions.common import AtomsNoBinaryFound


logger = logging.getLogger("atoms.utils.command")


class CommandUtils:

    @staticmethod
    def is_flatpak() -> bool:
        """
        Check if Atoms Core is running on a flatpak environment.
        """
        return "FLATPAK_ID" in os.environ

    @staticmethod
    def get_flatpak_command(command: list) -> list:
        """
        Returns a flatpak-spawn command for the given command.
        """
        binary_path = shutil.which("flatpak-spawn")
        return [binary_path, "--host"] + command

    @staticmethod
    def flatpak_host_which(binary: str) -> str:
        """
        Returns the path to the binary in the host system using flatpak-spawn
        to escape the sandbox. Atoms Core must be running in a flatpak
        environment which has permission to talk with org.freedesktop.Flatpak.

        :param binary: The binary to find in the host system.
        :return: The path to the binary in the host system.
        """
        try:
            proc = subprocess.check_output(
                CommandUtils.get_flatpak_command(["which", binary])
            )
            return proc.decode("utf-8").strip()
        except (FileNotFoundError, AtomsNoBinaryFound):
            return
        except subprocess.CalledProcessError:
            logger.warning("Atoms has no access to org.freedesktop.Flatpak")
            return

    @staticmethod
    def which(binary: str, allow_flatpak_host: bool = False) -> str:
        """
        Returns the path to the binary in the host system.

        :param binary: The binary to find in the host system.
        :param allow_flatpak_host: Whether to search the host system if Atoms 
               Core is running in a flatpak environment.
        """
        if allow_flatpak_host and CommandUtils.is_flatpak():
            return CommandUtils.flatpak_host_which(binary)
        return shutil.which(binary)
    
    @staticmethod
    def remove_formatting(output: str) -> str:
        """
        Remove formatting from the output.

        :param output: The output to remove formatting from.
        
        Credits: Martijn Pieters
                 <https://stackoverflow.com/a/14693789>
        """
        _output = copy.copy(output)
        try:
            ansi_escape = re.compile(r'''
                \x1B  # ESC
                (?:   # 7-bit C1 Fe (except CSI)
                    [@-Z\\-_]
                |     # or [ for CSI, followed by a control sequence
                    \[
                    [0-?]*  # Parameter bytes
                    [ -/]*  # Intermediate bytes
                    [@-~]   # Final byte
                )
            ''', re.VERBOSE)
            return ansi_escape.sub('', output)
        except TypeError:
            return _output

    @staticmethod
    def get_valid_command(command: list, allow_flatpak_host: bool = False) -> list:
        """
        Returns the command with the absolute path to the binary. The command
        list can contain a tuple of the form (binary, type), the type is used
        to determine where the method should search for the binary:
        - "bin" - search in the running system
        - "ext_bin" - search in the running system and the host system if
                      running in a flatpak environment.

        :param command: The command to find the absolute path to the binary.
        :param allow_flatpak_host: Whether to return a flatpak-spawn command if
                running in a flatpak environment.
        """
        _command = []

        for part in command:
            _part, _type = part, None

            if isinstance(part, tuple):
                _part, _type = part

            if _type == "bin":
                _part = CommandUtils.which(_part)
            elif _type == "ext_bin":
                _part = CommandUtils.which(_part, allow_flatpak_host=True)

            _part = CommandUtils.remove_formatting(_part)
            _command.append(_part)

        if allow_flatpak_host and CommandUtils.is_flatpak():
            _command = CommandUtils.get_flatpak_command(_command)

        return _command

    @staticmethod
    def run_command(
        command: list,
        output: bool = False,
        wait: bool = False,
        allow_flatpak_host: bool = False
    ) -> Union[str, None]:
        """
        Runs the command and returns the output.

        :param command: The command to run.
        :param output: Whether to return the output of the command.
        :param wait: Whether to wait for the command to finish.
        :param allow_flatpak_host: Whether to run the command in the host 
                     system if running in a flatpak environment.
        """
        _command = CommandUtils.get_valid_command(command, allow_flatpak_host)
        proc = subprocess.Popen(_command, stdout=subprocess.PIPE)

        if output:
            res = proc.communicate()[0].decode("utf-8")
            return CommandUtils.remove_formatting(res)

        if wait:
            proc.wait()

    @staticmethod
    def check_call(command: list, allow_flatpak_host: bool = False, ignore_errors: bool = False):
        """
        Runs the command and returns the output.

        :param command: The command to run.
        :param allow_flatpak_host: Whether to run the command in the host 
                     system if running in a flatpak environment.
        :param ignore_errors: Whether to ignore CalledProcessError.
        """
        _command = CommandUtils.get_valid_command(command, allow_flatpak_host)
        if ignore_errors:
            with contextlib.suppress(subprocess.CalledProcessError):
                subprocess.check_call(_command)
        else:
            subprocess.check_call(_command)
