# result.py
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

class ResultModel:

    def __init__(self, status: bool = False, data: dict = None, message: str = None):
        if data is None:
            data = {}

        if message is None:
            message = ''

        self.__status = status
        self.__data = data
        self.__message = message

    @property
    def status(self) -> bool:
        return self.__status

    @property
    def data(self) -> dict:
        return self.__data

    @property
    def message(self) -> str:
        return self.__message
        