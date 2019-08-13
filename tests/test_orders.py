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


import pytest

import dataverse


good_orders = [
    {
        "duration": 90,
        "is_buy_order": True,
        "issued": "2019-08-12T03:40:11Z",
        "location_id": 60004588,
        "min_volume": 1,
        "order_id": 5485158629,
        "price": 6.11,
        "range": "station",
        "system_id": 30002510,
        "type_id": 34,
        "volume_remain": 30000000,
        "volume_total": 30000000,
    },
    {
        "duration": 90,
        "is_buy_order": True,
        "issued": "2019-08-10T18:42:29Z",
        "location_id": 60004588,
        "min_volume": 1,
        "order_id": 5483786885,
        "price": 6.1,
        "range": "station",
        "system_id": 30002510,
        "type_id": 34,
        "volume_remain": 150000000,
        "volume_total": 150000000,
    },
]


@pytest.fixture
def bad_order():
    return {
        "duration": 90,
        "is_buy_order": True,
        "issued": "2019-08-12T03:40:11Z",
        "location_id": 60004588,
        "min_volume": 1,
        "order_id": 5485158629,
        "price": 6.11,
        "range": 999,
        "system_id": 30002510,
        "type_id": 34,
        "volume_remain": 30000000,
        "volume_total": 30000000,
    }


class TestOrders(object):
    def test_make_order_bad(self, bad_order):
        assert bad_order, None
