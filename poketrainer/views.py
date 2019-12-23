import base64
import logging
import requests

from flask import redirect, render_template, request, session
from requests_oauthlib import OAuth2Session

from poketrainer.app import flask_app
from poketrainer.api.syncs.fitbit import _generate_fitbit_token, \
    FITBIT_CALLBACK_URI


LOGGER = logging.getLogger(__name__)


@flask_app.route('/ui/collection/')
def collection():
    pokemon = requests.get(request.host_url + 'api/collection').json()
    return render_template('collection.html', pokemon=pokemon)


@flask_app.route('/ui/team/')
def team():
    pokemon = requests.get(request.host_url + 'api/team').json()
    return render_template('collection.html', pokemon=pokemon)


@flask_app.route('/fitbit_login/')
def fitbit_login():
    return _generate_fitbit_token()

@flask_app.route('/fitbitCallback')
def fitbit_callback():

    id_secret = (f'{flask_app.config["FITBIT_CLIENT_ID"]}:'
                 f'{flask_app.config["FITBIT_CLIENT_SECRET"]}')

    # see https://dev.fitbit.com/build/reference/web-api/oauth2/#refreshing-tokens  # noqa
    # for why we have to do this base64 stuff
    b64_creds = (base64.encodebytes(bytes(id_secret, 'utf8'))
                 .decode('utf8')
                 .rstrip())

    auth_header = {'Authorization': f'Basic {b64_creds}',
                   'Content-Type': 'application/x-www-form-urlencoded'}

    post_params = {'grant_type': 'authorization_code',
                   'code': request.args.get('code'),
                   'redirect_uri': request.host_url + FITBIT_CALLBACK_URI}

    # request the actual access token
    token = requests.post('https://api.fitbit.com/oauth2/token',
                          headers=auth_header, params=post_params).json()

    LOGGER.debug(token)

    # for some reason this fails with 'Missing access token'
    # c.f. https://github.com/requests/requests-oauthlib/issues/324
    # oauth = OAuth2Session(client_id=flask_app.config['FITBIT_CLIENT_ID'],
    #         redirect_uri=request.host_url + '/fitbitCallback/',
    #         scope=['activity'])

    # token = oauth.fetch_token(
    #     token_url='https://api.fitbit.com/oauth2/token',
    #     authorization_response=request.url,
    #     include_client_id=True,
    #     client_secret=flask_app.config['FITBIT_CLIENT_SECRET'])

    session.update(
        FITBIT_REFRESH_TOKEN=token['refresh_token'])

    return redirect('/ui/collection/')
