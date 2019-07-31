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

from marshmallow import Schema, fields, post_load

from . import EVE_ONLINE_BASE_URL, _cache


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
        graphic_id=None,
        dogma_attributes=None,
        dogma_effects=None,
        icon_id=None,
        market_group_id=None,
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
    def __init__(self, region_id=None, name=None, description=None, constellations=[]):
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


_typeSchema = TypeSchema()


@_cache.memoize(typed=True, expire=600)
def get_types() -> dict:
    payload = {}
    r = requests.get(f"{EVE_ONLINE_BASE_URL}/universe/types?datasource=tranquility", params=payload)

    return r.json()


@_cache.memoize(typed=True, expire=600)
def get_type(type_id: int) -> Type:
    payload = {}
    r = requests.get(f"{EVE_ONLINE_BASE_URL}/universe/types/{type_id}?datasource=tranquility", params=payload)

    return _typeSchema.load(r.json())
