from poketrainer.app import db, ma
from poketrainer.experience import get_base_exp


class Pokemon(db.Model):
    __tablename__ = 'pokemon'
    uid = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String(32))
    level = db.Column(db.Integer)
    experience = db.Column(db.Integer)
    team_uid = db.Column(db.Integer, db.ForeignKey('team.uid'), nullable=True)

    def _exp_up(self, exp):
        """Add experience to this pokemon, handling side effects"""

        self.experience += exp

        while get_base_exp(self.species, self.level) < self.experience:
            self._level_up()

    def _level_up(self):
        """Gain level"""
        self.level += 1


class PokemonSchema(ma.ModelSchema):
    class Meta:
        model = Pokemon
        sqla_session = db.session
        include_fk = True


class Team(db.Model):
    __tablename__ = 'team'
    uid = db.Column(db.Integer, primary_key=True)
    pokemon = db.relationship('Pokemon')

    def __init__(self, *args, **kwargs):
        """Commit immediately so that default values are populated"""
        super(Team, self).__init__(*args, **kwargs)
        db.session.add(self)
        db.session.commit()


class TeamSchema(ma.ModelSchema):
    class Meta:
        model = Team
        sqla_session = db.session
