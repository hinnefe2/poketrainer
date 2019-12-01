import datetime
import logging
import math

from poketrainer.app import db, ma
from poketrainer.config import STEPS_PER_ENCOUNTER


LOG = logging.getLogger(__name__)


class StepRecord(db.Model):
    __tablename__ = 'step_records'
    record_date = db.Column(db.DateTime, primary_key=True)
    updated_at = db.Column(db.DateTime)
    steps = db.Column(db.Integer)


class StepRecordSchema(ma.ModelSchema):
    class Meta:
        model = StepRecord
        sqla_session = db.session


class StepCounter(db.Model):
    __tablename__ = 'step_counter'
    uid = db.Column(db.Integer, primary_key=True)
    steps = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime)

    def __init__(self, *args, **kwargs):
        """Commit immediately so that default values are populated."""
        super(StepCounter, self).__init__(*args, **kwargs)
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Update the counter of total steps."""
        old_steps = self.steps
        self.steps = db.session.query(db.func.sum(StepRecord.steps)).scalar()
        self.updated_at = datetime.datetime.utcnow()
        db.session.commit()

        n_encounters = (math.floor(self.steps / STEPS_PER_ENCOUNTER) -
                        math.floor(old_steps / STEPS_PER_ENCOUNTER))

        LOG.debug(f'old steps: {old_steps}')
        LOG.debug(f'new steps: {self.steps}')
        LOG.debug(f'number of encounters from this update: {n_encounters}')

        return n_encounters


class StepCounterSchema(ma.ModelSchema):
    class Meta:
        model = StepCounter
        sqla_session = db.session
