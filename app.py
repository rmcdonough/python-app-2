#!/usr/bin/env python

"""
Example of a painfully trivial Flask application without setting up uWSGI, and
otherwise doing dumb things
"""

import logging
import json_logging
import random
import socket
import sys
from flask import Flask, jsonify, send_file


app = Flask(__name__)
json_logging.ENABLE_JSON_LOGGING = True
json_logging.init(framework_name='flask')
json_logging.init_request_instrument(app)
logger = logging.getLogger("test-logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))


UNICORN1 = 'unicorn1.jpg'
UNICORN2 = 'unicorn2.gif'
UNICORN3 = 'unicorn3.jpg'
UNICORNS = [UNICORN1, UNICORN2, UNICORN3]


@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route('/unicorn1.jpg')
def unicorn1():
    return send_file(UNICORN1, mimetype='image/jpeg')


@app.route('/unicorn2.gif')
def unicorn2():
    return send_file(UNICORN2, mimetype='image/gif')


@app.route('/unicorn3.jpg')
def unicorn3():
    return send_file(UNICORN3, mimetype='image/jpeg')


@app.route('/random')
def random_unicorn():
    return send_file(random.choice(UNICORNS))


@app.route('/list')
def list_unicorns():
    return jsonify({'unicorns': UNICORNS})


@app.route('/health_check')
def health_check():
    return jsonify({'status': 'ok', 'backend': socket.gethostname()}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')

