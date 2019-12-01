import datetime as dt
import requests as req

from dateutil import parser
from flask import request

from poketrainer.app import db
from poketrainer.models.records import (
    StepRecord, StepRecordSchema, StepCounter)


def _query_fitbit_api(date):
    """Retrieve step data from the fitbit API"""

    date_str = date.date().isoformat()

    # TODO: make this pull from the real API
    dummy = {'2019-10-20': 8000,
             '2019-10-21': 9000,
             '2019-10-22': 10000}

    return {'steps': dummy.get(date_str, 5000)}


def get(date=None):
    """Get step data from the database"""

    query = StepRecord.query.order_by(StepRecord.updated_at)

    if date is not None:
        query = query.filter(StepRecord.record_date == date)

    return StepRecordSchema(many=True).dump(query.all())


def post(date):
    """Add or update a record pulled from a step tracker"""

    date = parser.parse(date)

    fitbit_resp = _query_fitbit_api(date)

    record = StepRecord(
        record_date=date,
        updated_at=dt.datetime.utcnow(),
        steps=fitbit_resp['steps'])

    db.session.merge(record)
    db.session.commit()

    counter = StepCounter.query.get(1) or StepCounter()
    n_encounters = counter.update()

    for _ in range(n_encounters):
        req.post(request.host_url + 'api/encounters')

    return None, 201
