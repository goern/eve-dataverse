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
import json
import http

import daiquiri
import requests

from marshmallow import Schema, ValidationError, fields, post_load


from . import common, _cache
from .universe import Region, RegionSchema


_LOGGER = daiquiri.getLogger(__name__)


_regionSchema = RegionSchema()


def load_all_regions() -> list:
    """Load all Regions from the database file."""
    allRegions = []

    _LOGGER.debug("loading Regions from JSON file...")

    with open("regions.json") as file:
        data = json.load(file)

        if data is not None:
            for region in data:
                allRegions.append(RegionSchema().load(region))

        else:
            _LOGGER.error("Can't read Regions from JSON file.")

    _LOGGER.debug(f"loaded {len(allRegions)} Regions from JSON file...")

    return allRegions


@_cache.memoize(typed=True, expire=600)
def get_regions() -> list:
    return common.get_objects(f"/universe/regions/?datasource=tranquility")


@_cache.memoize(typed=True, expire=600)
def get_region(region_id: int) -> Region:
    result = None

    # TODO we should handle errors and rate limiting...
    try:
        # this will return a list with one element...
        r = common.get_objects(f"/universe/regions/{region_id}?datasource=tranquility")
        result = _regionSchema.load(r)

    except ValidationError as err:
        _LOGGER.error(err.messages)

    except Exception as e:  # TODO this is way to fuzzy
        _LOGGER.error(e)
        raise e

    return result
