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
import shutil

from atoms_core.utils.command import CommandUtils
from atoms_core.exceptions.common import AtomsNoBinaryFound


class ServicectlWrapper:

    def __init__(self):
        self.__servicectl_path = self.__find_binary_path("servicectl")
        self.__serviced_path = self.__find_binary_path("serviced")

    def __find_binary_path(self, binary: str) -> str:
        return CommandUtils.which(binary)

    def install_to_path(self, path: str):
        if not self.is_supported:
            return

        if not os.path.exists(path):
            os.makedirs(path)

        if os.path.exists(os.path.join(path, "servicectl")):
            os.remove(os.path.join(path, "servicectl"))
        shutil.copy(self.__servicectl_path, path)

        if os.path.exists(os.path.join(path, "serviced")):
            os.remove(os.path.join(path, "serviced"))
        shutil.copy(self.__serviced_path, path)
        
    def link_to_systemctl(self, path: str):
        if not self.is_supported:
            return

        with open(os.path.join(path, "etc/bash.bashrc"), "a") as bashrc:
            bashrc.write(f"alias systemctl=/usr/local/bin/servicectl")

    @property
    def is_supported(self) -> bool:
        return self.__servicectl_path is not None \
            and self.__serviced_path is not None
