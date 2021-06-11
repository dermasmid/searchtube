#!/bin/python3
from flask import Flask, request, render_template
import gotube
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__, static_url_path='/var/www/gotube/web')

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)


@app.route('/')
def hello():
    channels = gotube.utils.get_channels()
    return render_template('index.html', channels= channels)


@app.route('/search')
@limiter.limit('15/minute')
def search():
    q = request.args.get('q')
    channel_id = request.args.get('channel_id')

    if channel_id == '0':
        try:
            channel_id = gotube.utils.get_channels()[0]['channel_id']
        except IndexError:
            # there's no channels added
            channel_id = ''
    if gotube.utils.channel_is_in_db(channel_id):
        try:
            results = gotube.search.search(channel_id, q)
        except:
            results = []
        return {'data': results}
    else:
        return {'data': []}
