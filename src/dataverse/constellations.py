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

from . import common, _cache
from .universe import Constellation, Position, ConstellationSchema, PositionSchema


_LOGGER = daiquiri.getLogger(__name__)


_schema = ConstellationSchema()


@_cache.memoize(typed=True, expire=600)
def get_constellation(constellation_id: int) -> Constellation:
    result = None

    try:
        # this will return a list with one element...
        r = common.get_objects(f"/universe/constellations/{constellation_id!s}?datasource=tranquility")
        _LOGGER.debug(r)
        result = _schema.load(r)

    except ValidationError as err:
        _LOGGER.error(err.messages)

    except Exception as e:  # TODO this is way to fuzzy
        _LOGGER.error(e)
        raise e

    return result
