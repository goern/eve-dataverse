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

import daiquiri
import requests


from marshmallow import ValidationError


from . import common, _cache


_LOGGER = daiquiri.getLogger(__name__)


def load_all_orders() -> list:
    """Load all Orders from the database file."""
    allOrders = []

    _LOGGER.debug("loading Orders from JSON file...")

    with open("orders.json") as file:
        data = json.load(file)

        if data is not None:
            for o in data:
                try:
                    allOrders.append(OrderSchema().load(o))
                except ValidationError as e:
                    _LOGGER.error(e)
                    continue
        else:
            _LOGGER.error("Can't read Orders from JSON file.")

    _LOGGER.debug(f"loaded {len(allOrders)} Orders from JSON file...")

    return allOrders


@_cache.memoize(typed=True, expire=600)
def get_order_history(region_id: int, type_id: int) -> dict:
    result = None

    _LOGGER.debug(f"getting market order history for Region {region_id} and Type {type_id}")

    try:
        # this will return a list with one element...
        r = common.get_objects(f"/markets/{region_id}/history?datasource=tranquility&type_id={type_id}")
        _LOGGER.debug(r)
        result = r

    except Exception as e:  # TODO this is way to fuzzy
        _LOGGER.error(e)
        raise e

    return result


@_cache.memoize(typed=True, expire=600)
def get_orders(region_id: int, order_type: str, type_id: int) -> dict:
    """Get all Orders for the given Region, Order Type and Type."""
    result = None

    _LOGGER.debug(f"getting market orders for Region {region_id} and Type {type_id}, Order Type: {order_type}")

    try:
        # this will return a list with one element...
        r = common.get_objects(
            f"/markets/{region_id}/orders?datasource=tranquility&order_type={order_type}&type_id={type_id}"
        )
        _LOGGER.debug(r)
        result = r

    except Exception as e:  # TODO this is way to fuzzy
        _LOGGER.error(e)
        raise e

    return result


@_cache.memoize(typed=True, expire=600)
def get_order(order_id: int) -> dict:
    """Get the Order by ID."""
    result = None

    _LOGGER.debug(f"getting market order {order_id}")

    return result
