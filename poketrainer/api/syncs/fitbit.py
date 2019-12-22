import base64
import logging

import requests

from requests_oauthlib import OAuth2Session
from poketrainer.app import flask_app


def generate_fitbit_token():
    """Generate a new fitbit access token using a refresh token.

    This function uses an OAuth refresh token stored in the Flask app.config.

    Note that OAuth refresh tokens are only valid for a single use, so once
    used in this function a refresh token will need to be replaced. However,
    a successful response will include a new refresh token.

    Returns
    -------
    fitbit_token: dict
        Access token with keys [access_token, expires_in, refresh_token,
        scope, token_type, user_id]
    """

    id_secret = (f'{flask_app.config["FITBIT_CLIENT_ID"]}:'
                 f'{flask_app.config["FITBIT_CLIENT_SECRET"]}')

    # see https://dev.fitbit.com/build/reference/web-api/oauth2/#refreshing-tokens  # noqa
    # for why we have to do this base64 stuff
    b64_creds = (base64.encodebytes(bytes(id_secret, 'utf8'))
                 .decode('utf8')
                 .rstrip())

    auth_header = {'Authorization': f'Basic {b64_creds}',
                   'Content-Type': 'application/x-www-form-urlencoded'}

    post_params = {'grant_type': 'refresh_token',
                   'refresh_token': flask_app.config['FITBIT_REFRESH_TOKEN']}

    # request the actual access token
    new_token = requests.post('https://api.fitbit.com/oauth2/token',
                              headers=auth_header, params=post_params).json()

    if 'errors' in new_token:
        logging.ERROR(new_token)

    # update the app config with the new refresh token
    flask_app.config.update(FITBIT_REFRESH_TOKEN=new_token['refresh_token'])

    return new_token


def query_fitbit(day):

    token_dict = generate_fitbit_token()

    headers = {'Accept-Language': 'en_US'}

    oauth = OAuth2Session(client_id=flask_app.config.get('FITBIT_CLIENT_ID'),
                          token=token_dict)

    activity = oauth.get(
        'https://api.fitbit.com/1/user/-/activities/date/'
        f'{day.isoformat()}.json',
        headers=headers).json()

    return activity
