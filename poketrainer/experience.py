"""This module contains functions for calculating Pokemon experience levels."""


def _fast(level):
    return 4 / 5 * level**3


def _medium_fast(level):
    return level**3


def _medium_slow(level):
    return 6 / 5 * level**3 - 15 * level**2 + 100 * level - 140


def _slow(level):
    return 5 / 4 * level**3


def get_level_function(species):
    """Get the experience leveling function for a given pokemon"""

    # TODO: pull this from pokemondb.net
    return _medium_slow


def get_base_exp(species, level):
    """Get the base experience for a given pokemon species and level"""

    level_fn = get_level_function(species)

    return max([0, level_fn(level)])
