# distrobox.py
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
import shutil
import datetime

from atoms_core.utils.command import CommandUtils
from atoms_core.exceptions.podman import AtomsFailToCreateContainer


class DistroboxWrapper:

    def __init__(self):
        self.__binary_path = self.__find_binary_path()

    def __find_binary_path(self) -> str:
        return CommandUtils.which("distrobox")

    def get_containers(self) -> list:
        containers = {}
        command = [
            self.__binary_path,
            "list"
        ]

        output = CommandUtils.run_command(command, output=True)\
            .strip().split("\n")[1:]

        for line in output:
            _id, _name, _, _image = line.split("|")
            containers[_id] = {
                "image": _image.strip(),
                "name": _name.strip(),
                "creation_date": datetime.datetime.now().isoformat(),  # TODO: send PR to implement this
            }

        return containers

    def get_distrobox_command_for_container(
        self,
        container_id: str,
        command: list = None,
        working_directory: str = None
    ) -> list:
        if command is None:
            command = []
        else:
            command = ["--"] + command

        command = [
            self.__binary_path,
            "enter",
            container_id,
        ] + command

        return CommandUtils.get_valid_command(command)

    def destroy_container(self, container_id: str, container_name: str):
        self.stop_container(container_id)
        command = [self.__binary_path, "rm", "-f", container_name]
        CommandUtils.run_command(command)

    def stop_container(self, container_id: str):
        command = [self.__binary_path, "stop", "-f", container_id]
        CommandUtils.run_command(command)
    
    def new_container(self, name: str, image: str) -> str:
        command = [
            self.__binary_path, "create", 
            "--image", image,
            "--name", name
        ]
        try:
            CommandUtils.run_command(command, output=True, wait=True)
        except Exception as e:
            # TODO: improve error message
            raise AtomsFailToCreateContainer(str(e))

        _containers = self.get_containers()
        for _id, _container in _containers.items():
            if _container["name"] == name:
                return _id

        raise AtomsFailToCreateContainer(
            "A container with name '{}' was not found after creation. Somethings goes wrong.".format(name)
        )


    @property
    def is_supported(self) -> bool:
        return self.__binary_path is not None
