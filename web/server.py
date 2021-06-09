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
    return render_template('index.html')


@app.route('/search')
@limiter.limit('15/minute')
def search():
    q = request.args.get('q')
    return {'data': gotube.search.search('UCXv-co3EYHF7aOH4A93qAHQ', q)}
