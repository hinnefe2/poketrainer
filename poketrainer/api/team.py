from poketrainer.app import db
from poketrainer.config import MAX_TEAM_SIZE
from poketrainer.models.pokemon import Team, Pokemon, PokemonSchema


def get(team_uid=1):

    team = Team.query.get(team_uid) or Team()

    return PokemonSchema(many=True).dump(team.pokemon), 200


def post(pokemon_uid, team_uid=1):

    team = Team.query.get(team_uid) or Team()

    if len(team.pokemon) >= MAX_TEAM_SIZE:
        return "Team is full", 409

    pokemon = Pokemon.query.filter(Pokemon.uid == pokemon_uid).first()
    pokemon.team_uid = team_uid

    db.session.merge(pokemon)
    db.session.commit()

    return None, 201


def delete(pokemon_uid):

    pokemon = Pokemon.query.filter(Pokemon.uid == pokemon_uid).first()
    pokemon.team_uid = None

    db.session.merge(pokemon)
    db.session.commit()

    return None, 200
