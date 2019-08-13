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


"""This has all the Schemata and Classes for things we get from ESI."""


import os
import logging
import json
import time

import daiquiri
import requests

from marshmallow import Schema, ValidationError, fields, post_load

from . import common, _cache
from .universe import Type, TypeSchema


_LOGGER = daiquiri.getLogger(__name__)


_schema = TypeSchema()


def load_all_types() -> list:
    """Load all Types from the database file."""
    allTypes = []
    start_time = time.time()

    _LOGGER.debug("loading Types from JSON file...")

    with open("types.json") as file:
        data = json.load(file)

        if data is not None:
            for t in data:
                try:
                    allTypes.append(TypeSchema().load(t))
                except ValidationError as e:
                    _LOGGER.error(e)
                    continue
        else:
            _LOGGER.error("Can't read Types from JSON file.")

    end_time = time.time()
    elapsed = end_time - start_time

    _LOGGER.debug(f"loaded {len(allTypes)} Types from JSON file, time elapsed {elapsed}...")

    return allTypes


@_cache.memoize(typed=True, expire=600)
def get_types() -> list:
    return common.get_objects(f"/universe/types?datasource=tranquility")


@_cache.memoize(typed=True, expire=600)
def get_type(type_id: int) -> Type:
    result = None

    try:
        # this will return a list with one element...
        r = common.get_objects(f"/universe/types/{type_id!s}?datasource=tranquility")
        _LOGGER.debug(r)
        result = _schema.load(r)

    except ValidationError as err:
        _LOGGER.error(err.messages)

    except Exception as e:  # TODO this is way to fuzzy
        _LOGGER.error(e)
        raise e

    return result
