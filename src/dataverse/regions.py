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

from marshmallow import Schema, ValidationError, fields, post_load


from . import EVE_ONLINE_BASE_URL, _cache


_LOGGER = daiquiri.getLogger(__name__)


class Region:
    def __init__(self, region_id=None, name=None, description=None, constellations=[]):
        self.region_id = region_id
        self.name = name
        self.description = description
        self.constellations = constellations

    def __str__(self):
        return f"{self.region_id}: {self.name}, {self.description}, constellations: {self.constellations}"


class RegionSchema(Schema):
    region_id = fields.Integer(required=True)
    name = fields.String(required=True)
    description = fields.String()
    constellations = fields.List(fields.Integer(), required=True)

    @post_load
    def make_region(self, data, **kwargs):
        return Region(**data)


_regionSchema = RegionSchema()


@_cache.memoize(typed=True, expire=600)
def get_regions() -> list:
    payload = {}
    r = requests.get(f"{EVE_ONLINE_BASE_URL}/universe/regions/?datasource=tranquility", params=payload)

    return r.json()


@_cache.memoize(typed=True, expire=600)
def get_region(region_id: int) -> Region:
    payload = {}

    # TODO we should handle errors and rate limiting...
    r = requests.get(f"{EVE_ONLINE_BASE_URL}/universe/regions/{region_id}?datasource=tranquility", params=payload)

    result = None

    try:
        result = _regionSchema.load(r.json())
    except ValidationError as err:
        _LOGGER.error(err.messages)

    return result
