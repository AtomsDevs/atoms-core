# distribution.py
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
import re
import uuid
import requests
import tempfile

from atoms_core.exceptions.distribution import AtomsUnreachableRemote, AtomsMisconfiguredDistribution
from atoms_core.utils.command import CommandUtils
from atoms_core.utils.hash import HashUtils


class AtomDistribution:
    distribution_id: str
    name: str
    logo: str
    remote_structure: str
    remote_hash_structure: str
    architectures: dict

    def __init__(
        self,
        distribution_id: str,
        name: str,
        logo: str,
        releases: list,
        remote_structure: str,
        remote_hash_structure: str,
        remote_hash_type: str,
        architectures: dict,
        root: str,
        container_image_name: str,
        motd: str = None
    ):
        self.distribution_id = distribution_id
        self.name = name
        self.logo = logo
        self.releases = releases
        self.remote_structure = remote_structure
        self.remote_hash_structure = remote_hash_structure
        self.remote_hash_type = remote_hash_type
        self.architectures = architectures
        self.root = root
        self.container_image_name = container_image_name
        self.motd = motd

    def __str__(self):
        return f"Distribution {self.name}"

    def get_remote(self, architecture: str, release: str) -> str:
        return self.remote_structure.format(release, architecture)

    def get_remote_hash(self, architecture: str, release: str) -> str:
        if self.remote_hash_structure is None:
            return
            
        return self.remote_hash_structure.format(release, architecture)

    def get_image_name(self, architecture: str, release: str) -> str:
        remote = HashUtils.get_string_hash(self.get_remote(architecture, release), "sha1")
        _repr = f"{self.distribution_id}-{release}-{architecture}-{remote}"
        return _repr.replace(".", "-").replace("_", "-").replace(" ", "-").lower()

    def get_remote_image_name(self, architecture: str, release: str) -> str:
        remote = self.get_remote(architecture, release)
        return os.path.basename(remote)

    def read_remote_hash(self, architecture: str, release: str) -> str:
        if self.remote_hash_structure is None:
            return

        remote_hash = self.get_remote_hash(architecture, release)
        response = requests.get(remote_hash)

        if response.status_code != 200:
            raise AtomsUnreachableRemote(remote_hash)

        content = response.text.split("\n")
        for line in content:
            if len(line) == 0:
                continue

            items = re.split(r"\s+", line, maxsplit=1)
            if len(items) == 1:
                return items[0]

            _hash, _file = items

            if self.get_remote_image_name(architecture, release) in _file.strip():
                return _hash.strip()
            raise AtomsMisconfiguredDistribution(
                "Hash mismatch or the sum file is not well formatted. Double check that the file name respect its remote.")

        raise ValueError(f"Unknown check_type method: {check_type}")

    def is_container_image(self, image: str) -> bool:
        return self.container_image_name in image
    
    def post_unpack(self, chroot: str):
        pass
    
    def set_motd(self, chroot: str):
        if self.motd:
            with open(os.path.join(chroot, "etc/profile"), "a") as f:
                f.write("cat /etc/motd\n")
            with open(os.path.join(chroot, "etc/motd"), "w") as f:
                f.write(self.motd)

    def _download_resource(self, url: str):
        temp_path = tempfile.gettempdir()
        temp_resource_folder = os.path.join(temp_path, str(uuid.uuid4()))
        temp_resource_file = os.path.join(temp_resource_folder, os.path.basename(url))

        os.makedirs(temp_resource_folder)

        with open(temp_resource_file, "wb") as f:
            response = requests.get(url, stream=True)
            if response.status_code != 200:
                raise AtomsUnreachableRemote(url)

            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()

        return temp_resource_file
    
    def _extract_resource(self, resource_file: str, path: str):
        if not os.path.exists(path):
            os.makedirs(path)

        CommandUtils.run_command(
            CommandUtils.get_valid_command([
                ("tar", "bin"),
                "-xf", resource_file, "-C", path
            ])
        )

    def _get_remote_dirs(self, url: str) -> list:
        response = requests.get(url)

        if response.status_code != 200:
            raise AtomsUnreachableRemote(url)

        html = response.text
        links = re.findall(r'<a href="(.*?)">(.*?)</a>', html)

        if len(links) == 0:
            raise AtomsMisconfiguredDistribution(f"No directories found in {url}")

        links = [link[1].replace('/', '').strip() for link in links]
        links = [link for link in links if link[:4].isdigit()]
        links.sort(reverse=True)
        return links

    def _get_latest_remote_dir(self, url: str) -> str:
        return self._get_remote_dirs(url)[0]
