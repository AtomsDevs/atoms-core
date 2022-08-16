# atoms.py
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

from atoms_core.entities.config import AtomsConfig
from atoms_core.entities.atom import Atom
from atoms_core.entities.atom_type import AtomType
from atoms_core.entities.instance import AtomsInstance
from atoms_core.utils.image import AtomsImageUtils
from atoms_core.wrappers.client_bridge import ClientBridge
from atoms_core.wrappers.distrobox import DistroboxWrapper


class AtomsBackend:
    __atoms: dict
    config: AtomsConfig

    def __init__(self, distrobox_support: bool = False, client_bridge: 'ClientBridge' = None):
        if client_bridge is None:
            client_bridge = ClientBridge()

        self.__config = AtomsConfig()
        self.__instance = AtomsInstance(self.__config, client_bridge)
        self.__distrobox_support = distrobox_support
        self.__atoms = self.__list_atoms()

    def __list_atoms(self) -> dict:
        atoms = {}
        for atom in os.listdir(self.__config.atoms_path):
            if atom.endswith(".atom"):
                atoms[atom] = Atom.load(self.__instance, atom)

        if self.__distrobox_support and self.has_distrobox_support:
            atoms.update(self.__list_distrobox_atoms())
        
        if "DEV_BASH" in os.environ:
            atoms["DEV_BASH"] = Atom.new_system_shell(self.__instance)

        return atoms

    def __list_distrobox_atoms(self) -> dict:
        atoms = {}
        containers = DistroboxWrapper().get_containers()

        if not containers:
            return atoms

        for container_id, info in containers.items():
            atoms[container_id] = Atom.load_from_container(
                self.__instance, info["creation_date"], info["name"], info["image"], container_id
            )
        return atoms

    def request_new_atom(
        self,
        name: str,
        atom_type: 'AtomType',
        distribution: 'AtomDistribution'=None,
        architecture: str=None,
        release: str=None,
        container_image: str=None,
        download_fn: callable = None,
        config_fn: callable = None,
        unpack_fn: callable = None,
        distrobox_fn: callable = None,
        finalizing_fn: callable = None,
        error_fn: callable = None
    ):
        if atom_type == AtomType.ATOM_CHROOT:
            return Atom.new(
                self.__instance, name, distribution, architecture, release,
                download_fn, config_fn, unpack_fn, finalizing_fn, error_fn
            )
        elif atom_type == AtomType.DISTROBOX_CONTAINER:
            return Atom.new_container(
                self.__instance, name, container_image, distrobox_fn, 
                finalizing_fn, error_fn
            )

    @property
    def atoms(self) -> dict:
        return self.__atoms

    @property
    def has_atoms(self) -> bool:
        return len(self.__atoms) > 0

    @property
    def local_images(self) -> list:
        return AtomsImageUtils.get_image_list(self.__config)

    @property
    def has_distrobox_support(self) -> bool:
        return DistroboxWrapper().is_supported

    @property
    def client_bridge(self) -> 'ClientBridge':
        return self.__client_bridge

    @property
    def instance(self) -> 'AtomsInstance':
        return self.__instance
