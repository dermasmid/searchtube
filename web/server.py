#!/bin/python3
from flask import Flask, request, render_template
import searchtube

app = Flask(__name__)


@app.route('/')
def hello():
    channels = searchtube.utils.get_channels()
    return render_template('index.html', channels= channels)


@app.route('/search')
def search():
    q = request.args.get('q')
    channel_id = request.args.get('channel_id')
    limit = request.args.get('limit', 0)

    if channel_id == '0':
        try:
            channel_id = searchtube.utils.get_channels()[0]['channel_id']
        except IndexError:
            # there's no channels added
            channel_id = ''
    if searchtube.utils.channel_is_in_db(channel_id):
        try:
            results = searchtube.search.search(channel_id, q, limit)
        except:
            results = []
        return {'data': results}
    else:
        return {'data': []}
