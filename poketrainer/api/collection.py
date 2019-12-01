from poketrainer.app import db
from poketrainer.models.pokemon import Pokemon, PokemonSchema
from poketrainer.experience import get_base_exp


def get():
    """Get the user's collection"""

    pokemon = Pokemon.query.all()

    return PokemonSchema(many=True).dump(pokemon), 200


def post(species, level):
    """Add a pokemon to the user's collection"""

    pokemon = Pokemon(species=species,
                      level=level,
                      experience=get_base_exp(species, level))

    db.session.add(pokemon)
    db.session.commit()

    return None, 201


def patch(uid, exp_gain):
    """Update a pokemon in the user's collection"""

    Pokemon.query.filter(Pokemon.uid == uid).first()._exp_up(exp_gain)
    db.session.commit()

    return None, 204
