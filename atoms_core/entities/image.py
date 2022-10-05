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
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar, destination)

        if self.root == "":
            return

        root = os.path.join(destination, self.root)

        for file in os.listdir(root):
            _file = os.path.join(root, file)
            shutil.move(_file, destination)

        os.rmdir(root)

    def destroy(self):
        os.remove(self.path)
