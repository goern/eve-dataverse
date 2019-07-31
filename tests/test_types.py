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


class TestTypes(object):
    def test_get_types(self):
        d = dataverse.types.get_types()

        assert isinstance(d, list)
        assert 2019 in d

    def test_get_type(self):
        d = dataverse.types.get_type(2019)

        assert isinstance(d, dataverse.universe.Type)
        assert d.group_id == 141
        assert d.market_group_id == 1558
        assert d.name == "Medium Cap Battery I Blueprint"
