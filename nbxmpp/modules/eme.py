# Copyright (C) 2018 Philipp Hörist <philipp AT hoerist.com>
#
# This file is part of nbxmpp.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; If not, see <http://www.gnu.org/licenses/>.

from nbxmpp.modules.base import BaseModule
from nbxmpp.namespaces import Namespace
from nbxmpp.structs import EMEData
from nbxmpp.structs import StanzaHandler


class EME(BaseModule):
    def __init__(self, client):
        BaseModule.__init__(self, client)

        self._client = client
        self.handlers = [
            StanzaHandler(name='message',
                          callback=self._process_eme,
                          ns=Namespace.EME,
                          priority=40)
        ]

    def _process_eme(self, _client, stanza, properties):
        encryption = stanza.getTag('encryption', namespace=Namespace.EME)
        if encryption is None:
            return

        name = encryption.getAttr('name')
        namespace = encryption.getAttr('namespace')
        if namespace is None:
            self._log.warning('No namespace on message')
            return

        properties.eme = EMEData(name=name, namespace=namespace)
        self._log.info('Found data: %s', properties.eme)
