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

from marshmallow import pprint

from dataverse import regions, markets

daiquiri.setup(level=logging.DEBUG)
_LOGGER = daiquiri.getLogger("eve_dataverse")


if __name__ == "__main__":
    _LOGGER.info("harvesting data...")

    regionSchema = regions.RegionSchema()

    region_ids = regions.get_regions()

    for region_id in region_ids:
        region = regions.get_region(region_id)

        if region is not None:
            pprint(regionSchema.dump(region))
