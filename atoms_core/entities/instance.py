# instance.py
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


class AtomsInstance:
    config: 'AtomsConfig'
    client_bridge: 'ClientBridge'

    def __init__(self, config: 'AtomsConfig', client_bridge: 'ClientBridge'):
        self.config = config
        self.client_bridge = client_bridge
