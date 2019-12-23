import logging
import requests as req

from collections import namedtuple

from flask import request
from numpy.random import choice, binomial


LOG = logging.getLogger(__name__)

Encounter = namedtuple(
    'Encounter', ['species', 'prob', 'min_lvl', 'max_lvl'])


def _sample_species(location):
    """Generate a pokemon encounter based on the player's location."""

    # TODO: make this scrape https://bulbapedia.bulbagarden.net/wiki/Kanto_Route_1#Generation_IV  # noqa

    lookup = {
        'route_1': [
            Encounter('pidgey', 0.55, 2, 4),
            Encounter('rattata', 0.45, 2, 4),
            ],
        'route_2': [
            Encounter('pidgey', 0.40, 3, 5),
            Encounter('rattata', 0.45, 2, 5),
            Encounter('caterpie', 0.15, 3, 5),
            ],
        }

    possible_encounters = lookup[location]

    # this is gross but choice() won't sample from more complicated objects
    [_idx] = choice([i for i, _ in enumerate(possible_encounters)],
                    p=[enc.prob for enc in possible_encounters],
                    size=1, replace=True)

    encounter = possible_encounters[_idx]

    [level] = choice(list(range(encounter.min_lvl, encounter.max_lvl)), 1)

    LOG.info(f'encountered a level {level} {encounter.species}')

    return encounter.species, level


def _capture_attempt(species, level):

    # TODO: make this a function of pokemon rarity, level, and player level
    return bool(binomial(1, 0.5))


def post():

    location = 'route_1'

    species, level = _sample_species(location)

    if _capture_attempt(species, level):
        LOG.info(f'caught a level {level} {species}!')
        req.post(request.host_url +
                 f'api/collection?species={species}&level={level}')
        return None, 201

    else:
        LOG.info(f'a level {level} {species} got away!')
        return None, 200
