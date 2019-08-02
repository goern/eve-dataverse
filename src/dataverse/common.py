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


"""These are common method to work w/ ESI."""


import os
import logging
import json
import time

import daiquiri
import requests

from marshmallow import Schema, ValidationError, fields, post_load

from . import EVE_ONLINE_BASE_URL, EVE_ONLINE_REQUEST_HEADERS, _cache, MissingRequiredArgumentError

_LOGGER = daiquiri.getLogger(__name__)


def get_objects(url: str = None) -> dict:
    """Get objects from ESI, doing pagination."""
    headers = EVE_ONLINE_REQUEST_HEADERS
    payload = {}
    responses = []
    pages = 1

    # TODO make sure url has no leading slash, as it is part of EVE_ONLINE_BASE_URL

    if url is None:
        raise MissingRequiredArgumentError(None, "required 'url' argemunt is missing")

    start_time = time.time()

    # TODO exception handling...
    r = requests.get(f"{EVE_ONLINE_BASE_URL}{url}", params=payload)
    response = r.json()

    # TODO we should handle rate limiting...

    try:
        pages = int(r.headers["X-Pages"])  # this might not be present
        objects_etag = r.headers["ETag"]  # pretty save that ETag is always present ;)

        _LOGGER.debug(f"{objects_etag}: {response}")
    except KeyError as e:
        _LOGGER.warning(f"Can't find Header 'X-Pages' in HTTP response object: {e}")

    if type(response) == list:
        responses.extend(response)
    else:
        responses = response

    for page in range(2, pages - 1):
        # TODO exception handling...
        r = requests.get(f"{EVE_ONLINE_BASE_URL}{url}&page={page}", params=payload, headers=headers)
        responses.extend(r.json())

    end_time = time.time()
    elapsed = end_time - start_time
    _LOGGER.debug(f"time elapsed to get all {len(responses)} objects: {elapsed}")

    return responses

