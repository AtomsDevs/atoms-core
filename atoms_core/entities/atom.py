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
import uuid
import shutil
import orjson
import tempfile
import datetime
import importlib

from atoms_core.exceptions.atom import AtomsWrongAtomData
from atoms_core.exceptions.download import AtomsHashMissmatchError
from atoms_core.exceptions.image import AtomsFailToDownloadImage
from atoms_core.exceptions.distribution import AtomsUnreachableRemote
from atoms_core.utils.paths import AtomsPathsUtils
from atoms_core.utils.image import AtomsImageUtils
from atoms_core.utils.distribution import AtomsDistributionsUtils
from atoms_core.utils.file import FileUtils
from atoms_core.wrappers.proot import ProotWrapper
from atoms_core.wrappers.podman import PodmanWrapper


class Atom:
    name: str
    distribution_id: str
    creation_date: str
    upate_date: str
    relative_path: str

    def __init__(
        self,
        instance: "AtomsInstance",
        name: str,
        distribution_id: str = None,
        relative_path: str = None,
        creation_date: str = None,
        update_date: str = None,
        podman_container_id: str = None,
        podman_container_image: str = None
    ):
        if update_date is None and podman_container_id:
            update_date = datetime.datetime.now().isoformat()
        elif update_date is None:
            update_date = creation_date

        self._instance = instance
        self.name = name
        self.distribution_id = distribution_id
        self.relative_path = relative_path
        self.creation_date = creation_date
        self.update_date = update_date
        self.podman_container_id = podman_container_id
        self.podman_container_image = podman_container_image
        self.__proot_wrapper = ProotWrapper()

        if podman_container_id:
            self.__podman_wrapper = PodmanWrapper()

    @classmethod
    def from_dict(cls, instance: "AtomsInstance", data: dict) -> "Atom":
        if None in [
            data.get("name"),
            data.get("distributionId"),
            data.get("creationDate"),
            data.get("updateDate"),
            data.get("relativePath")
        ]:
            raise AtomsWrongAtomData(data)
        return cls(
            instance,
            data['name'],
            data['distributionId'],
            data['relativePath'],
            data['creationDate'],
            data['updateDate']
        )

    @classmethod
    def load(cls, instance: "AtomsInstance", relative_path: str) -> "Atom":
        path = os.path.join(AtomsPathsUtils.get_atom_path(
            instance.config, relative_path), "atom.json")
        with open(path, "r") as f:
            data = orjson.loads(f.read())
        return cls.from_dict(instance, data)

    @classmethod
    def load_from_container(
        cls,
        instance: "AtomsInstance",
        creation_date: str,
        podman_container_names: str,
        podman_container_image: str,
        podman_container_id: str
    ) -> "Atom":
        return cls(
            instance,
            podman_container_names,
            creation_date=creation_date,
            podman_container_id=podman_container_id,
            podman_container_image=podman_container_image
        )

    @classmethod
    def new(
        cls,
        instance: 'AtomsInstance',
        name: str,
        distribution: 'AtomDistribution',
        architecture: str,
        release: str,
        download_fn: callable = None,
        config_fn: callable = None,
        unpack_fn: callable = None,
        finalizing_fn: callable = None,
        error_fn: callable = None
    ) -> 'Atom':
        # Get image
        try:
            image = AtomsImageUtils.get_image(
                instance, distribution, architecture, release, download_fn)
        except AtomsHashMissmatchError:
            if error_fn:
                instance.client_bridge.exec_on_main(error_fn, "Hash missmatch")
        except AtomsFailToDownloadImage:
            if error_fn:
                instance.client_bridge.exec_on_main(
                    error_fn, "Fail to download image, it might be a temporary problem")
        except AtomsUnreachableRemote:
            if error_fn:
                instance.client_bridge.exec_on_main(
                    error_fn, "Unreachable remote, it might be a temporary problem")

        # Create configuration
        if config_fn:
            instance.client_bridge.exec_on_main(config_fn, 0)

        date = datetime.datetime.now().isoformat()
        relative_path = str(uuid.uuid4()) + ".atom"
        atom_path = AtomsPathsUtils.get_atom_path(
            instance.config, relative_path)
        chroot_path = os.path.join(atom_path, "chroot")
        root_path = os.path.join(chroot_path, "root")
        atom = cls(instance, name, distribution.distribution_id,
                   relative_path, date)
        os.makedirs(chroot_path)

        if config_fn:
            instance.client_bridge.exec_on_main(config_fn, 1)

        # Unpack image
        if unpack_fn:
            instance.client_bridge.exec_on_main(unpack_fn, 0)

        image.unpack(chroot_path)
        os.makedirs(root_path, exist_ok=True)

        if unpack_fn:
            instance.client_bridge.exec_on_main(unpack_fn, 1)

        # Finalize and distro specific workarounds
        if finalizing_fn:
            instance.client_bridge.exec_on_main(finalizing_fn, 0)

        # workaround for unsigned repo in ubuntu (need to investigate the cause)
        if distribution.distribution_id == "ubuntu":
            with open(os.path.join(chroot_path, "etc/apt/sources.list"), "r") as f:
                sources = f.read()
            sources = sources.replace("deb ", "deb [trusted=yes] ")
            sources = sources.replace("deb-src ", "deb-src [trusted=yes] ")
            with open(os.path.join(chroot_path, "etc/apt/sources.list"), "w") as f:
                f.write(sources)
        shutil.copy2("/etc/resolv.conf",
                     os.path.join(chroot_path, "etc/resolv.conf"))
        atom.save()
        if finalizing_fn:
            instance.client_bridge.exec_on_main(finalizing_fn, 1)

        return atom

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "distributionId": self.distribution_id,
            "relativePath": self.relative_path,
            "creationDate": self.creation_date,
            "updateDate": self.update_date
        }

    def save(self):
        if self.is_podman_container:
            raise AtomsCannotSavePodmanContainers()

        path = os.path.join(self.path, "atom.json")
        with open(path, "wb") as f:
            f.write(orjson.dumps(self.to_dict(), f,
                    option=orjson.OPT_NON_STR_KEYS))

    def generate_command(self, command: list, environment: list = None, track_exit: bool = True) -> tuple:
        if self.is_podman_container:
            command, environment, working_directory = self.__generate_podman_command(
                command, environment)
        else:
            command, environment, working_directory = self.__generate_proot_command(
                command, environment)

        if track_exit:
            command = ["sh", self.__get_launcher_script()] + command

        return command, environment, working_directory

    def __generate_proot_command(self, command: list, environment: list = None) -> tuple:
        if environment is None:
            environment = []

        _command = self.__proot_wrapper.get_proot_command_for_chroot(
            self.fs_path, command)
        return _command, environment, self.root_path

    def __generate_podman_command(self, command: list, environment: list = None) -> tuple:
        if environment is None:
            environment = []

        _command = self.__podman_wrapper.get_podman_command_for_container(
            self.podman_container_id, command)
        return _command, environment, self.root_path

    def __get_launcher_script(self) -> str:
        script = """#!/bin/bash
while true; do
    clear
    $@
    read -n 1 -s -r -p "Press any [Key] to restart the Atom Console…";
done
"""
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
            f.write(script)
            return f.name

    def destroy(self):
        if self.is_podman_container:
            self.__podman_wrapper.destroy_container(self.podman_container_id)
            return

        # NOTE: might not be the best way to do this but shutil raises an
        #       error if has no permissions to remove the directory since
        #       the homedir is mounted in some way (not unmoutable).
        #       A better way would be stop the running proot process and
        #       then remove the directory, but since Atoms has a no track
        #       of the proot process, this is the best we can do for now.
        binary_path = shutil.which("rm")
        FileUtils.native_rm(self.path)

    def kill(self):
        if self.is_podman_container:
            self.__podman_wrapper.stop_container(self.podman_container_id)
            return

        pids = ProcUtils.find_proc_by_cmdline(self.relative_path)
        for pid in pids:
            pid.kill()

    def rename(self, new_name: str):
        if self.is_podman_container:
            raise AtomsCannotRenamePodmanContainers()
        self.name = new_name
        self.save()

    def stop_podman_container(self):
        PodmanWrapper().stop_container(self.podman_container_id)

    @property
    def path(self) -> str:
        if self.is_podman_container:
            return ""
        return AtomsPathsUtils.get_atom_path(self._instance.config, self.relative_path)

    @property
    def fs_path(self) -> str:
        if self.is_podman_container:
            return ""
        return os.path.join(
            AtomsPathsUtils.get_atom_path(
                self._instance.config, self.relative_path),
            "chroot"
        )

    @property
    def root_path(self) -> str:
        if self.is_podman_container:
            return ""
        return os.path.join(self.fs_path, "root")

    @property
    def distribution(self) -> 'AtomDistribution':
        if self.is_podman_container:
            return AtomsDistributionsUtils.get_distribution_by_container_image(self.podman_container_image)
        return AtomsDistributionsUtils.get_distribution(self.distribution_id)

    @property
    def enter_command(self) -> list:
        return self.generate_command([])

    @property
    def formatted_update_date(self) -> str:
        return datetime.datetime.strptime(
            self.update_date, "%Y-%m-%dT%H:%M:%S.%f"
        ).strftime("%d %B, %Y %H:%M:%S")

    @property
    def is_podman_container(self) -> bool:
        return self.podman_container_id is not None

    def __str__(self):
        if self.is_podman_container:
            return f"Atom {self.name} (podman container)"
        return f"Atom: {self.name}"
