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


"""This is just a Test."""


import os
import logging

import daiquiri
import requests

from marshmallow import ValidationError, Schema, fields, post_load

from . import EVE_ONLINE_BASE_URL, _cache


_LOGGER = daiquiri.getLogger(__name__)


class Position:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z


class Constellation:
    def __init__(self, constellation_id: int, name: str, position: Position, region_id: int, systems: list):
        self.constellation_id = constellation_id
        self.name = name
        self.position = position
        self.region_id = region_id
        self.systems = systems


class ConstellationPositionSchema(Schema):
    x = fields.Float(required=True)
    y = fields.Float(required=True)
    z = fields.Float(required=True)

    @post_load
    def make_position(self, data, **kwargs):
        return Position(**data)


class ConstellationSchema(Schema):
    constellation_id = fields.Integer(required=True)
    name = fields.String(required=True)
    position = fields.Nested(ConstellationPositionSchema, required=True)
    region_id = fields.Integer(required=True)
    systems = fields.List(fields.Integer())

    @post_load
    def make_constellation(self, data, **kwargs):
        return Constellation(**data)


_constellationSchema = ConstellationSchema()


@_cache.memoize(typed=True, expire=600)
def get_constellation(constellation_id: int) -> Constellation:
    payload = {}

    # TODO we should handle errors and rate limiting...
    r = requests.get(
        f"{EVE_ONLINE_BASE_URL}/universe/constellations/{constellation_id}?datasource=tranquility", params=payload
    )

    result = None

    try:
        result = _constellationSchema.load(r.json())
    except ValidationError as err:
        _LOGGER.error(err.messages)

    return result
