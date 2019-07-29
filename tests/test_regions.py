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


class TestRegions(object):
    def test_get_regions(self):
        regions = dataverse.regions.get_regions()

        assert isinstance(regions, list)
        assert 10000001 in regions

    def test_get_region(self):
        region = dataverse.regions.get_region(10000001)

        assert isinstance(region, dict)
        assert region["region_id"] == 10000001
        assert region["name"] == "Derelik"
