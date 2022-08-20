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
import subprocess
import shlex

from atoms_core.exceptions.distribution import AtomsUnreachableRemote, AtomsMisconfiguredDistribution


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

    def __str__(self):
        return f"Distribution {self.name}"

    def get_remote(self, architecture: str, release: str) -> str:
        return self.remote_structure.format(release, architecture)

    def get_remote_hash(self, architecture: str, release: str) -> str:
        if self.remote_hash_structure is None:
            return
            
        return self.remote_hash_structure.format(release, architecture)

    def get_image_name(self, architecture: str, release: str) -> str:
        _repr = f"{self.distribution_id}-{release}-{architecture}"
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
            _hash, _file = re.split(r"\s+", line, maxsplit=1)
            if self.get_remote_image_name(architecture, release) in _file.strip():
                return _hash.strip()
            raise AtomsMisconfiguredDistribution(
                "Hash mismatch or the sum file is not well formatted. Double check that the file name respect its remote.")

        raise ValueError(f"Unknown check_type method: {check_type}")

    def is_container_image(self, image: str) -> bool:
        return self.container_image_name in image
    
    def post_unpack(self, chroot: str):
        pass
    
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

        subprocess.run(["tar", "-xf", resource_file, "-C", path])
