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

import logging

from nbxmpp.protocol import Error
from nbxmpp.protocol import ERR_BAD_REQUEST
from nbxmpp.protocol import NodeProcessed
from nbxmpp.protocol import presence_types
from nbxmpp.util import StanzaHandler

log = logging.getLogger('nbxmpp.m.presence')


class BasePresence:
    def __init__(self, client):
        self._client = client
        self.handlers = [
            StanzaHandler(name='presence',
                          callback=self._process_presence_base,
                          priority=10),
        ]

    def _process_presence_base(self, _con, stanza, properties):
        properties.type = self._parse_type(stanza)
        properties.priority = self._parse_priority(stanza)
        properties.show = self._parse_show(stanza)
        properties.jid = stanza.getFrom()
        properties.id = stanza.getID()
        properties.status = stanza.getStatus()

        if properties.type == 'error':
            properties.error_code = stanza.getErrorCode()
            properties.error_message = stanza.getErrorMsg()

        own_jid = self._client.get_bound_jid()
        if own_jid == stanza.getFrom():
            properties.self_presence = True

    @staticmethod
    def _parse_priority(stanza):
        priority = stanza.getPriority()
        if priority is None:
            return 0

        try:
            priority = int(priority)
        except Exception:
            log.warning('Invalid priority value: %s', priority)
            log.warning(stanza)
            return 0

        if priority not in range(-128, 127):
            log.warning('Invalid priority value: %s', priority)
            log.warning(stanza)
            return 0

        return priority

    def _parse_type(self, stanza):
        type_ = stanza.getType()
        if type_ is None:
            return

        if type_ not in presence_types:
            log.warning('Presence with invalid type received')
            log.warning(stanza)
            self._client.send(Error(stanza, ERR_BAD_REQUEST))
            raise NodeProcessed
        return type_

    @staticmethod
    def _parse_show(stanza):
        show = stanza.getShow()
        if show not in ('chat', 'away', 'xa', 'dnd'):
            return
        return show
