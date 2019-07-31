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


import diskcache as dc


__version__ = "0.1.0-dev"
_USER_AGENT = f"b4dataverse/{__version__}"

_cache = dc.Cache("tmp")


EVE_ONLINE_BASE_URL = "https://esi.evetech.net/latest"
EVE_ONLINE_REQUEST_HEADERS = {"User-Agent": _USER_AGENT}
