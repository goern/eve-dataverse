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


"""This is a harvester for Eve Online Swagger API (aka ESI) data."""


import os
import logging
import json

import daiquiri
import requests
import click

from marshmallow import pprint

from dataverse import universe, regions, constellations, markets, types, common, __version__

daiquiri.setup(level=logging.DEBUG)
_LOGGER = daiquiri.getLogger("dataverse.harvester")

allRegions = []
allConstellations = []
allTypes = []


def harvest_constellation_data():
    _LOGGER.info("harvesting Constellation data...")

    schema = constellations.ConstellationSchema()

    for region in allRegions:
        for constellation_id in region.constellations:
            constellation = constellations.get_constellation(constellation_id)

            if constellation is not None:
                allConstellations.append(constellation)

    _LOGGER.debug("writing Constellations to JSON file...")
    with open("constellations.json", "w") as outfile:
        outfile.write(schema.dumps(allConstellations, many=True))


@click.group()
@click.version_option(version=__version__)
@click.option("--debug/--no-debug", default=False, envvar="DEBUG")
@click.pass_context
def cli(ctx=None, debug=True):
    print(f"This is Eve Online Dataverse harvester v{__version__}.")
    _LOGGER.debug("DEBUG mode is enabled!")


@cli.group(name="region")
@click.pass_context
def region_command(ctx):
    pass


@cli.group(name="constellation")
@click.pass_context
def constellation_command(ctx):
    pass


@cli.group(name="system")
@click.pass_context
def system_command(ctx):
    pass


@cli.group(name="planet")
@click.pass_context
def planet_command(ctx):
    pass


@cli.group(name="type")
@click.pass_context
def type_command(ctx):
    pass


@cli.group(name="order")
@click.pass_context
def order_command(ctx):
    pass


@region_command.command(name="get")
@click.option("--all", is_flag=True, default=False, help="get all Regions")
@click.option("--force", is_flag=True, default=False, help="forcing the cache to be cleared before harvesting")
@click.argument("id", required=False)
@click.pass_context
def region_command_get(ctx, all, force, id=None):
    """The `region get` sub-command."""
    _LOGGER.info("harvesting Region data...")

    schema = universe.RegionSchema()

    if force:
        _LOGGER.debug(f"clearing cache before harvesting")

        raise NotImplementedError

    if all:
        _LOGGER.debug("harvesting all Region data...")

        region_ids = regions.get_regions()

        for region_id in region_ids:
            region = regions.get_region(region_id)

            if region is not None:
                allRegions.append(region)

        _LOGGER.debug("writing Regions to JSON file...")
        with open("regions.json", "w") as outfile:
            outfile.write(schema.dumps(allRegions, many=True))

    elif id is not None:
        _LOGGER.debug(f"harvesting Region {id} data...")

        raise NotImplementedError
    elif id is None:
        _LOGGER.error("a Region ID is required!")


@region_command.command(name="find")
@click.argument("name", required=True)
@click.option("--json-output", is_flag=True, default=False, help="print search result as JSON")
@click.pass_context
def region_command_find_by_name(ctx, json_output, name=None):
    """The `region find` sub-command."""
    _LOGGER.debug("finding Region...")

    for region in regions.load_all_regions():
        if region.name.upper() == name.upper():
            if json_output:
                print(universe.RegionSchema().dumps(region))
            else:
                print(region)


@type_command.command(name="get")
@click.option("--all", is_flag=True, default=False, help="get all Types")
@click.option("--force", is_flag=True, default=False, help="forcing the cache to be cleared before harvesting")
@click.argument("id", required=False)
@click.pass_context
def type_command_get(ctx, all, force, id=None):
    """The `type get` sub-command."""
    _LOGGER.info("harvesting Type data...")

    schema = universe.TypeSchema()

    if force:
        _LOGGER.debug(f"clearing cache before harvesting")

        raise NotImplementedError

    if all:
        _LOGGER.debug("harvesting all Type data...")

        type_ids = types.get_types()

        for type_id in type_ids:
            type_object = types.get_type(type_id)

            if type_object is not None:
                allTypes.append(type_object)

        _LOGGER.debug("writing Types to JSON file...")
        with open("types.json", "w") as outfile:
            outfile.write(schema.dumps(allTypes, many=True))

    elif id is not None:
        _LOGGER.debug(f"harvesting Type {id} data...")

        raise NotImplementedError
    elif id is None:
        _LOGGER.error("a Type ID is required!")


@type_command.command(name="find")
@click.argument("search-string", required=True)
@click.option(
    "--search-in-attribute",
    type=click.Choice(["type_id", "name", "description"]),
    default="type_id",
    help="which attribute to search thru",
)
@click.option("--json-output", is_flag=True, default=False, help="print search result as JSON")
@click.pass_context
def type_command_find_by_id(ctx, json_output, search_in_attribute, search_string=None):
    """The `type find` sub-command."""
    _LOGGER.debug("finding Type...")

    for t in types.load_all_types():
        # TODO implement to search thru name or description
        if t.type_id == search_string:
            if json_output:
                print(universe.TypeSchema().dumps(t))
            else:
                print(t)


@order_command.command(name="get")
@click.option("--region-id", required=True, help="Region ID to get the market orders from")
@click.option("--type-id", default=34, help="limit getting market orders to this Type ID")
@click.option("--order-type", type=click.Choice(["all", "sell", "buy"]), default="all", help="the order type to get")
@click.option("--force", is_flag=True, default=False, help="forcing the cache to be cleared before harvesting")
@click.pass_context
def order_command_get(ctx, force, type_id, order_type, region_id=None):
    """The `order get` sub-command."""
    _LOGGER.info("getting Market data...")

    if force:
        _LOGGER.debug(f"clearing cache before harvesting")

        raise NotImplementedError

    if (region_id is not None) and (type_id is not None):
        orders = markets.get_orders(region_id=region_id, type_id=type_id, order_type=order_type)

        print(orders)


if __name__ == "__main__":
    cli()
