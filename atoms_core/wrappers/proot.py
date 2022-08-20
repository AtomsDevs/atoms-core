# proot.py
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

import os
import uuid
import shutil
import tempfile
import subprocess
from pathlib import Path

from atoms_core.utils.command import CommandUtils
from atoms_core.exceptions.common import AtomsNoBinaryFound


class ProotWrapper:

    def __init__(self):
        self.__binary_path = self.__find_binary_path()

    def __find_binary_path(self) -> str:
        return CommandUtils.which("proot")

    def get_proot_command_for_chroot(
        self,
        chroot_path: str,
        command: list = None,
        working_directory: str = None,
        bind_mounts: list = None,
    ) -> list:
        if "DEV_BASH" in os.environ:
            return CommandUtils.get_valid_command([("bash", "bin")])

        if command is None:
            command = []

        if working_directory is None:
            working_directory = "/"

        _command = [
            ("env", "bin"), "-i", 
            "HOSTNAME=atom", 
            f"TERM=xterm-256color", 
            "HOME=/root",
            "TMPDIR=/tmp",
            f"DISPLAY={os.environ['DISPLAY']}",
        ]

        if "ATOMS_NO_SECCOMP" in os.environ:
            _command.append("PROOT_NO_SECCOMP=1")

        # PATH is unset at this point, no binaries will be found, so we set it
        # to the default paths if the a command is provided
        if command:
            _command += ["PATH=/sbin:/usr/sbin:/bin:/usr/bin:/usr/local/sbin:/usr/local/bin"]
        
        _command += [
            self.__binary_path,
            "-w", working_directory,

            # the following pass the current user and group id to the chroot
            # it's currently disabled as I'm trying to figure the user as root
            # "-i", f"{os.getuid()}:{os.getgid()}",

            "-0",
            "--kill-on-exit",
            "-r", chroot_path,
            "-b", "/etc/host.conf:/etc/host.conf",
            "-b", "/etc/hosts:/etc/hosts",
            "-b", "/etc/nsswitch.conf:/etc/nsswitch.conf",
            "-b", "/etc/resolv.conf:/etc/resolv.conf",
            "-b", "/etc/timezone:/etc/timezone",
            "-b", "/etc/localtime:/etc/localtime",
            "-b", "/dev:/dev",
            "-b", "/dev/urandom:/dev/urandom",
            "-b", "/proc:/proc",
            "-b", "/sys:/sys",
            "-b", "/tmp:/tmp",
            "-b", f"{Path.home()}:{Path.home()}",
            "-b", f"/run/user/{os.getuid()}:/run/user/{os.getuid()}",
            "-b", "/usr/lib/x86_64-linux-gnu/GL/lib/dri/:/usr/lib/xorg/modules/dri",

            # the following are handled by the Atom instance
            #"-b", "/usr/share/themes:/usr/share/themes",
            #"-b", "/usr/share/fonts:/usr/share/fonts",
            #"-b", "/usr/share/icons:/usr/share/icons",
        ]

        if bind_mounts is not None:
            for bind_mount in bind_mounts:
                host_mount, chroot_mount = bind_mount
                _command.append("-b")
                _command.append(f"{host_mount}:{chroot_mount}")
        
        # passwd and group cannot be binded, this will replace the existing
        # files, invalidating users/groups made by the user in the chroot
        # here we make a temporary copy of the files. merge them and bind
        # the temporary instead of the original
        # temp_path = tempfile.gettempdir()
        # chroot_passwd = os.path.join(chroot_path, "etc/passwd")
        # chroot_group = os.path.join(chroot_path, "etc/group")
        # system_passwd = os.path.join("/", "etc/passwd")
        # system_group = os.path.join("/", "etc/group")
        # temp_passwd = os.path.join(temp_path, f"passwd_{uuid.uuid4()}")
        # temp_group = os.path.join(temp_path, f"group_{uuid.uuid4()}")

        # system_passwd_rows = []
        # system_group_rows = []

        # with open(system_passwd, "r") as f:
        #     system_passwd_rows = f.readlines()

        # with open(system_group, "r") as f:
            # system_group_rows = f.readlines()
            
        # shutil.copyfile(chroot_passwd, temp_passwd)
        # shutil.copyfile(chroot_group, temp_group)

        # with open(temp_passwd, "a+") as f:
        #     rows = f.readlines()
        #     for row in system_passwd_rows:
        #         if row not in rows:
        #             f.write(row)

        # with open(temp_group, "a+") as f:
            # rows = f.readlines()
            # for row in system_group_rows:
                # if row not in rows:
                    # f.write(row)

        # command = _command + [
            # passwd disabled, I'm trying to make the user root of the chroot
            # "-b", f"{temp_passwd}:/etc/passwd",
            # "-b", f"{temp_group}:/etc/group",
        # ] + command

        command = _command + command

        return CommandUtils.get_valid_command(command)
