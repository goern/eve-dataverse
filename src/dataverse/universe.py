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


"""This has all the Schemata and Classes for things we get from ESI."""


import os
import logging

import daiquiri
import requests

from marshmallow import Schema, ValidationError, fields, post_load


_LOGGER = daiquiri.getLogger(__name__)


class Type:
    def __init__(
        self,
        type_id,
        group_id,
        name,
        description,
        published,
        capacity=None,
        graphic_id=-1,  # TODO is it ok to set all these to -1 as a default?!
        dogma_attributes=[],
        dogma_effects=[],
        icon_id=-1,
        market_group_id=-1,
        mass=None,
        packaged_volume=None,
        portion_size=None,
        radius=None,
        volume=None,
    ):
        self.type_id = type_id
        self.graphic_id = graphic_id
        self.group_id = group_id
        self.name = name
        self.description = description
        self.published = published
        self.capacity = capacity
        self.dogma_attributes = dogma_attributes
        self.dogma_effects = dogma_effects
        self.icon_id = icon_id
        self.market_group_id = market_group_id
        self.mass = mass
        self.packaged_volume = packaged_volume
        self.portion_size = portion_size
        self.radius = radius
        self.volume = volume

    def __str__(self):
        return f"Type {self.type_id}: {self.name}, {self.description}"


class Position:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z


class Constellation:
    def __init__(self, constellation_id: int, name: str, position: Position, region_id: int, systems: list):
        self.constellation_id = constellation_id
        self.name = name
        self.position = position
        self.region_id = region_id
        self.systems = systems


class System:
    def __init__(
        self,
        constellation_id: int,
        name: str,
        position: Position,
        security_class: str,
        security_status: float,
        star_id: int,
        stargates: list,
        stations: list,
        system_id: int,
        planets: list,
    ):
        self.constellation_id = constellation_id
        self.name = name
        self.position = position
        self.security_class = security_class
        self.security_status = security_status
        self.star_id = star_id
        self.stargates = stargates
        self.stations = stations
        self.system_id = system_id


class SystemPlanets:
    def __init__(self, planet_id: int, asteroid_belts: list = [], moons: list = []):
        self.planet_id = planet_id
        self.asteroid_belts = asteroid_belts
        self.moons = moons


class Region:
    def __init__(self, region_id=None, name=None, description="", constellations=[]):
        self.region_id = region_id
        self.name = name
        self.description = description
        self.constellations = constellations

    def __str__(self):
        return f"{self.region_id}: {self.name}, {self.description}, constellations: {self.constellations}"


class RegionSchema(Schema):
    region_id = fields.Integer(required=True)
    name = fields.String(required=True)
    description = fields.String()
    constellations = fields.List(fields.Integer(), required=True)

    @post_load
    def make_region(self, data, **kwargs):
        return Region(**data)


class PositionSchema(Schema):
    x = fields.Float(required=True)
    y = fields.Float(required=True)
    z = fields.Float(required=True)

    @post_load
    def make_position(self, data, **kwargs):
        return Position(**data)


class ConstellationSchema(Schema):
    constellation_id = fields.Integer(required=True)
    name = fields.String(required=True)
    position = fields.Nested(PositionSchema, required=True)
    region_id = fields.Integer(required=True)
    systems = fields.List(fields.Integer())

    @post_load
    def make_constellation(self, data, **kwargs):
        return Constellation(**data)


class SystemPlanetsSchema(Schema):
    planet_id = fields.Integer(required=True)
    asteroid_belts = fields.List(fields.Integer())
    moons = fields.List(fields.Integer())

    @post_load
    def make_system_planets(self, data, **kwargs):
        return SystemPlanets(**data)


class SystemSchema(Schema):
    constellation_id = fields.Integer(required=True)
    name = fields.String(required=True)
    planets = fields.List(fields.Nested(SystemPlanetsSchema), required=True)
    position = fields.Nested(PositionSchema, required=True)
    security_class = fields.String()
    security_status = fields.Float()
    star_id = fields.Integer()
    stargates = fields.List(fields.Integer())
    stations = fields.List(fields.Integer())
    system_id = fields.Integer(required=True)

    @post_load
    def make_system(self, data, **kwargs):
        return System(**data)


class DogmaAttributeSchema(Schema):
    attribute_id = fields.Integer(required=True)
    value = fields.Float(required=True)


class DogmaEffectSchema(Schema):
    effect_id = fields.Integer(required=True)
    is_default = fields.Boolean(required=True)


class TypeSchema(Schema):
    capacity = fields.Integer()
    description = fields.String(required=True)
    dogma_attributes = fields.List(fields.Nested(DogmaAttributeSchema))
    dogma_effects = fields.List(fields.Nested(DogmaEffectSchema))
    graphic_id = fields.Integer()
    group_id = fields.Integer(required=True)
    icon_id = fields.Integer()
    market_group_id = fields.Integer()
    mass = fields.Float()
    name = fields.String(required=True)
    packaged_volume = fields.Float()
    portion_size = fields.Integer()
    published = fields.Boolean(required=True)
    radius = fields.Integer()
    type_id = fields.Integer(required=True)
    volume = fields.Float()

    @post_load
    def make_type(self, data, **kwargs):
        return Type(**data)


class Character:
    def __init__(
        self,
        character_id,
        birthday,
        bloodline_id,
        corporation_id,
        gender,
        name,
        race_id,
        alliance_id=None,
        ancestry_id=None,
        description=None,
        faction_id=None,
        security_status=None,
        title=None,
    ):
        self.character_id = character_id
        self.alliance_id = alliance_id
        self.ancestry_id = ancestry_id
        self.birthday = birthday
        self.bloodline_id = bloodline_id
        self.corporation_id = corporation_id
        self.description = description
        self.faction_id = faction_id
        self.gender = gender
        self.name = name
        self.race_id = race_id
        self.security_status = security_status
        self.title = title

    def __str__(self):
        return f"Character {self.character_id}: {self.name}"


class CharacterSchema(Schema):
    character_id = fields.Integer(required=True)
    alliance_id = fields.Integer()
    ancestry_id = fields.Integer()
    birthday = fields.String(required=True)
    bloodline_id = fields.Integer(required=True)
    corporation_id = fields.Integer(required=True)

    description = fields.String()
    faction_id = fields.Integer()
    gender = fields.String(required=True)
    name = fields.String(required=True)
    race_id = fields.Integer()
    security_status = fields.Float()
    title = fields.String()

    @post_load
    def make_character(self, data, **kwargs):
        return Character(**data)


class Killmail:
    """This is Killmail information as provided by https://zkillboard.com/api/, enriched with ESI data."""

    def __init__(
        self,
        killmail_id,
        killmail_hash,
        character,
        location_id,
        fitted_value,
        total_value,
        points,
        npc,
        solo,
        awox,
        time,
        solar_system_id,
        position,
        victim,
    ):
        self.killmail_id = killmail_id
        self.killmail_hash = killmail_hash
        self.character = character
        self.location_id = location_id
        self.fitted_value = fitted_value
        self.total_value = total_value
        self.points = points
        self.npc = npc
        self.solo = solo
        self.awox = awox
        self.time = time
        self.solar_system_id = solar_system_id
        self.position = position
        self.victim = victim

    def __str__(self):
        return f"Killmail id: {self.killmail_id}, hash: {self.killmail_hash}, location: {self.location_id}, time: {self.time}, fitted Value: {self.fitted_value}, total Value: {self.total_value}, character: {self.character.name}, victim: {self.victim.name}"


class KillmailSchema(Schema):
    killmail_id = fields.Integer(required=True)
    killmail_hash = fields.String(required=True)
    character = fields.Nested(CharacterSchema, required=True)
    location_id = fields.Integer(required=True)
    fitted_value = fields.Integer()
    total_value = fields.Integer()
    points = fields.Integer()
    npc = fields.Boolean()
    solo = fields.Boolean()
    awox = fields.Boolean()
    time = fields.AwareDateTime()
    solar_system_id = fields.Integer()
    position = fields.Nested(PositionSchema)
    victim = fields.Nested(CharacterSchema)

    @post_load
    def make_killmail(self, data, **kwargs):
        return Killmail(**data)
