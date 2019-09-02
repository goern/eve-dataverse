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


"""These are the tests for zkillboard killmails."""


import pytest

import dataverse


class TestKillmails(object):
    def test_get_killmails_wrong_character_id(self):
        with pytest.raises(dataverse.exceptions.WrongRequiredArgumentError):
            # pylint: disable=unused-variable
            k = dataverse.killmail.get_killmails(-1)
            k = dataverse.killmail.get_killmails(0)

    def test_get_killmails(self):
        k = dataverse.killmail.get_killmails(2115480998)

        assert isinstance(k, list)
        assert len(k) > 0, "got at least one killmail"
        assert isinstance(k[0], dataverse.universe.Killmail)

    def test_get_killmails_paginated(self):
        k = dataverse.killmail.get_killmails(268946627)

        assert isinstance(k, list)
        assert len(k) > 0, "got at least one killmail"
        assert isinstance(k[0], dataverse.universe.Killmail)
