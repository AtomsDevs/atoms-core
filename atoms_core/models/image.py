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
import datetime

from atoms_core.utils.file import FileUtils


class ImageModel:

    def __init__(
        self,
        name: str,
        path: str,
        root: str = None,
    ):
        self.name = name
        self.path = path
        self.root = root

    @property
    def size(self):
        return os.path.getsize(self.path)

    @property
    def human_size(self):
        return FileUtils.get_human_size(self.size)
    
    @property
    def date(self):
        return os.path.getmtime(self.path)
    
    @property
    def formatted_date(self):
        return datetime.datetime.fromtimestamp(self.date).strftime("%Y-%m-%d %H:%M:%S")
