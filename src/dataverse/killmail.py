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


"""This has all the killmail related Schemata and Classes for things we get from ESI."""


import os
import logging
import json

import daiquiri
import requests

from . import common, _cache, APIEndpoint
from .exceptions import WrongRequiredArgumentError
from .universe import KillmailSchema, CharacterSchema

from marshmallow import Schema, ValidationError, fields, post_load


_LOGGER = daiquiri.getLogger(__name__)


_schema = KillmailSchema()


@_cache.memoize(typed=True, expire=600)
def get_killmails(character_id: int) -> list:
    """Retriev all Killmails for the given Charakter ID."""
    killmails = list()
    need_to_get_more = True
    page = 1

    if character_id < 1:
        raise WrongRequiredArgumentError(None, character_id)

    try:
        while need_to_get_more:
            _killmails = common.get_objects2(APIEndpoint.ZKILLBOARD, f"/kills/characterID/{character_id}/page/{page}/")
            _LOGGER.debug(_killmails)

            # if there is no killmail on this page... BREAK BREAK BREAK!!
            if len(_killmails) == 0:
                need_to_get_more = False

            _LOGGER.debug(f"killmail: {json.dumps(_killmails)}")
            _LOGGER.debug(f"number of killmail: {len(_killmails)}")

            _character = common.get_character(character_id)
            _LOGGER.debug(f"character: {json.dumps(_character)}")

            _character["character_id"] = character_id

            for killmail in _killmails:
                _evekillmail = common.get_objects2(
                    APIEndpoint.EVE_ONLINE,
                    f"killmails/{killmail['killmail_id']}/{killmail['zkb']['hash']}/?datasource=tranquility",
                )

                # TODO refactor this out to get the cache going
                _victim = common.get_objects2(
                    APIEndpoint.EVE_ONLINE,
                    f"/characters/{_evekillmail['victim']['character_id']}/?datasource=tranquility",
                )
                _victim["character_id"] = _evekillmail["victim"]["character_id"]

                _LOGGER.debug(_victim)
                _LOGGER.debug(_character)

                km = dict()
                km["killmail_id"] = killmail["killmail_id"]
                km["killmail_hash"] = killmail["zkb"]["hash"]
                km["time"] = _evekillmail["killmail_time"]
                km["solar_system_id"] = _evekillmail["solar_system_id"]
                km["position"] = _evekillmail["victim"]["position"]
                km["character"] = _character
                km["victim"] = _victim
                km["location_id"] = killmail["zkb"]["locationID"]
                km["fitted_value"] = killmail["zkb"]["fittedValue"]
                km["total_value"] = killmail["zkb"]["totalValue"]
                km["points"] = killmail["zkb"]["points"]
                km["npc"] = killmail["zkb"]["npc"]
                km["solo"] = killmail["zkb"]["solo"]
                km["awox"] = killmail["zkb"]["awox"]

                k = _schema.load(km)
                killmails.append(k)

            # let's walk on to the next page...
            page = page + 1

    except Exception as e:
        _LOGGER.exception(e)

    _LOGGER.debug(f"total numner of killmails: {len(killmails)}")

    return killmails
