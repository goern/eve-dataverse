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
