#!/usr/bin/env python3
#
# Copyright(C) 2019 Christoph Görn
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>


"""This has all the killmail related Schemata and Classes for things we get from ESI."""


import os
import logging

import daiquiri
import requests

from marshmallow import Schema, ValidationError, fields, post_load


_LOGGER = daiquiri.getLogger(__name__)


class Killmail:
    """This is Killmail information as provided by https://zkillboard.com/api/"""

    def __init__(self, killmail_id, location_id, _hash, fitted_value, total_value, points, npc, solo, awox):
        self.killmail_id = killmail_id
        self.location_id = location_id
        self._hash = _hash
        self.fitted_value = fitted_value
        self.total_value = total_value
        self.points = points
        self.npc = npc
        self.solo = solo
        self.awox = awox

    def __str__(self):
        return f"Killmail {self.killmail_id}: hash: {self._hash}"


class KillmailSchema(Schema):
    killmail_id = fields.Integer(required=True)
    location_id = fields.Integer(required=True)
    _hash = fields.String(required=True)
    fitted_value = fields.Integer()
    total_value = fields.Integer()
    points = fields.Integer()
    npc = fields.Boolean()
    solo = fields.Boolean()
    awox = fields.Boolean()

    @post_load
    def make_killmail(self, data, **kwargs):
        return Killmail(**data)
