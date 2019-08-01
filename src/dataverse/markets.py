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


from . import EVE_ONLINE_BASE_URL, EVE_ONLINE_REQUEST_HEADERS, _cache


_LOGGER = daiquiri.getLogger(__name__)


@_cache.memoize(typed=True, expire=600)
def get_order_history(region_id: int, type_id: int) -> dict:
    payload = {}
    headers = EVE_ONLINE_REQUEST_HEADERS
    result = None

    _LOGGER.debug(f"getting market order history for Region {region_id} and Type {type_id}")

    # TODO we should handle rate limiting...
    try:
        r = requests.get(
            f"{EVE_ONLINE_BASE_URL}/markets/{region_id}/history?datasource=tranquility&type_id={type_id}",
            params=payload,
            headers=headers,
        )

        result = r.json()

    except Exception as e:  # TODO this is way to fuzzy
        _LOGGER.error(e)

    return result


@_cache.memoize(typed=True, expire=600)
def get_orders(region_id: int, order_type: str, type_id: int) -> dict:
    """Get all Orders for the given Region, Order Type and Type."""
    payload = {}
    headers = EVE_ONLINE_REQUEST_HEADERS
    result = None

    _LOGGER.debug(f"getting market orders for Region {region_id} and Type {type_id}, Order Type: {order_type}")

    # TODO we should handle rate limiting...
    try:
        r = requests.get(
            f"{EVE_ONLINE_BASE_URL}/markets/{region_id}/orders?datasource=tranquility&order_type={order_type}&type_id={type_id}&page=1",  # TODO pagination
            params=payload,
            headers=headers,
        )

        pages = r.headers["X-Pages"]

        _LOGGER.debug(f"the result has {pages} pages...")

        result = r.json()

    except Exception as e:  # TODO this is way to fuzzy
        _LOGGER.error(e)

    return result
