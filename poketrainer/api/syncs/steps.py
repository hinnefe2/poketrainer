import datetime as dt
import logging
import requests as req

from dateutil import parser
from flask import request

from poketrainer.app import db
from poketrainer.models.records import (
    StepRecord, StepRecordSchema, StepCounter)
from poketrainer.api.syncs.fitbit import query_fitbit


LOGGER = logging.getLogger(__name__)


def _query_fitbit_api(date):
    """Retrieve step data from the fitbit API"""

    resp = query_fitbit(date)

    return resp['summary']['steps']


def get(date=None):
    """Get step data from the database"""

    query = StepRecord.query.order_by(StepRecord.updated_at)

    if date is not None:
        query = query.filter(StepRecord.record_date == date)

    return StepRecordSchema(many=True).dump(query.all())


def post(date=None):
    """Add or update a record pulled from a step tracker"""

    # use the current date if none was specified
    date = parser.parse(date) if date else dt.date.today()

    try:
        steps = _query_fitbit_api(date)
    except ValueError as e:
        LOGGER.exception(e)
        return None, 401

    LOGGER.debug(f'Pulled {steps} steps for {date.isoformat()}')

    # record the step count for this date or update the existing step count if
    # it already exists
    record = StepRecord(
        record_date=date,
        updated_at=dt.datetime.utcnow(),
        steps=steps)

    db.session.merge(record)
    db.session.commit()

    counter = StepCounter.query.get(1) or StepCounter()
    n_encounters = counter.update()

    LOGGER.debug(f'{steps} generated {n_encounters} encounters')

    for _ in range(n_encounters):
        req.post(request.host_url + 'api/encounters')

    return None, 201
