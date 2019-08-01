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

from . import EVE_ONLINE_BASE_URL, EVE_ONLINE_REQUEST_HEADERS, _cache
from .universe import Type, TypeSchema


_LOGGER = daiquiri.getLogger(__name__)


_typeSchema = TypeSchema()


def load_all_types() -> list:
    """Load all Types from the database file."""
    allTypes = []

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

    _LOGGER.debug(f"loaded {len(allTypes)} Types from JSON file...")

    return allTypes


@_cache.memoize(typed=True, expire=600)
def get_types() -> dict:
    headers = EVE_ONLINE_REQUEST_HEADERS
    payload = {}
    responses = []

    start_time = time.time()

    # FIXME exception handling...
    r = requests.get(f"{EVE_ONLINE_BASE_URL}/universe/types?datasource=tranquility", params=payload)
    pages = int(r.headers["X-Pages"])

    responses.extend(r.json())

    for page in range(2, pages - 1):
        r = requests.get(
            f"{EVE_ONLINE_BASE_URL}/universe/types?datasource=tranquility&page={page}", params=payload, headers=headers
        )
        responses.extend(r.json())

    end_time = time.time()
    elapsed = end_time - start_time
    _LOGGER.debug(f"time elapsed to get all Types: {elapsed}")

    _LOGGER.debug(f"harvested {len(responses)} Types.")
    return responses


@_cache.memoize(typed=True, expire=600)
def get_type(type_id: int) -> Type:
    payload = {}
    headers = EVE_ONLINE_REQUEST_HEADERS
    result = None

    # TODO we should handle rate limiting...
    try:
        r = requests.get(
            f"{EVE_ONLINE_BASE_URL}/universe/types/{type_id}?datasource=tranquility", params=payload, headers=headers
        )

        result = _typeSchema.load(r.json())

    except ValidationError as err:
        _LOGGER.error(err.messages)

    except Exception as e:  # TODO this is way to fuzzy
        _LOGGER.error(e)

    return result
