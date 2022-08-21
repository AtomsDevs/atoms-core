# atom.py
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
import datetime

from atoms_core.utils.paths import AtomsPathsUtils
from atoms_core.utils.distribution import AtomsDistributionsUtils


class AtomModel:

    def __init__(
        self,
        instance: "AtomsInstance",
        name: str,
        distribution_id: str = None,
        relative_path: str = None,
        creation_date: str = None,
        update_date: str = None,
        container_id: str = None,
        container_image: str = None,
        system_shell: bool = False,
        bind_themes: bool = False,
        bind_icons: bool = False,
        bind_fonts: bool = False,
        bind_extra_mounts: list = None,
    ):
        if update_date is None and (container_id or system_shell):
            update_date = datetime.datetime.now().isoformat()
        elif update_date is None:
            update_date = creation_date

        self._instance = instance
        self._name = name.strip()
        self._distribution_id = distribution_id
        self._relative_path = relative_path
        self._creation_date = creation_date
        self._update_date = update_date
        self._container_id = container_id
        self._container_image = container_image
        self._system_shell = system_shell
        self._bind_themes = bind_themes
        self._bind_icons = bind_icons
        self._bind_fonts = bind_fonts
        self._bind_extra_mounts = bind_extra_mounts or []

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def relative_path(self) -> str:
        return self._relative_path
    
    @property
    def creation_date(self) -> str:
        return self._creation_date

    @property
    def update_date(self) -> str:
        return self._update_date
    
    @property
    def distribution_id(self) -> str:
        return self._distribution_id

    @property
    def path(self) -> str:
        if self.is_distrobox_container or self._system_shell:
            return ""
        return AtomsPathsUtils.get_atom_path(self._instance.config, self._relative_path)

    @property
    def fs_path(self) -> str:
        if self.is_distrobox_container or self._system_shell:
            return ""
        return os.path.join(
            AtomsPathsUtils.get_atom_path(self._instance.config, self._relative_path),
            "chroot"
        )

    @property
    def root_path(self) -> str:
        if self.is_distrobox_container or self._system_shell:
            return ""
        return os.path.join(self.fs_path, "root")

    @property
    def distribution(self) -> 'AtomDistribution':
        if self.is_distrobox_container:
            return AtomsDistributionsUtils.get_distribution_by_container_image(self._container_image)
        if self._system_shell:
            return Host()
        return AtomsDistributionsUtils.get_distribution(self._distribution_id)

    @property
    def enter_command(self) -> list:
        return self.generate_command([])
    
    @property
    def untracked_enter_command(self) -> list:
        return self.generate_command([], track_exit=False)

    @property
    def formatted_update_date(self) -> str:
        return datetime.datetime.strptime(
            self._update_date, "%Y-%m-%dT%H:%M:%S.%f"
        ).strftime("%d %B, %Y %H:%M:%S")

    @property
    def is_distrobox_container(self) -> bool:
        return self._container_id is not None

    @property
    def is_system_shell(self) -> bool:
        return self._system_shell
    
    @property
    def aid(self) -> str:
        if self.is_distrobox_container or self._system_shell:
            return self._container_id
        return self._relative_path
    
    @property
    def container_id(self) -> str:
        return self._container_id

    @property
    def container_image(self) -> str:
        return self._container_image

    @property
    def bind_themes(self) -> bool:
        return self._bind_themes

    @property
    def bind_icons(self) -> bool:
        return self._bind_icons

    @property
    def bind_fonts(self) -> bool:
        return self._bind_fonts
    
    @property
    def bind_extra_mounts(self) -> list:
        return self._bind_extra_mounts

    @property
    def bind_mounts(self) -> list:
        mounts = []
        if self._bind_themes:
            mounts.append(("/usr/share/themes", "/usr/share/themes"))
        if self._bind_icons:
            mounts.append(("/usr/share/icons", "/usr/share/icons"))
        if self._bind_fonts:
            mounts.append(("/usr/share/fonts", "/usr/share/fonts"))
        if self._bind_extra_mounts:
            mounts += self._bind_extra_mounts
        return mounts