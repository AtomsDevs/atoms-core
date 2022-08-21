# image.py
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
import tarfile

from atoms_core.exceptions.image import AtomsImageMissingRoot
from atoms_core.models.image import ImageModel


class AtomImage(ImageModel):

    def __init__(self, name: str, path: str, root: str = None):
        super().__init__(name, path, root)

    def unpack(self, destination: str):
        if self.root is None:
            raise AtomsImageMissingRoot(self.name)

        if not os.path.exists(destination):
            os.makedirs(destination)

        with tarfile.open(self.path) as tar:
            tar.extractall(destination)

        if self.root == "":
            return

        root = os.path.join(destination, self.root)

        for file in os.listdir(root):
            _file = os.path.join(root, file)
            shutil.move(_file, destination)

        os.rmdir(root)

    def destroy(self):
        os.remove(self.path)
