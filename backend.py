 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import json
from feed_maker import *
from bson import json_util
from flask import Flask, url_for, send_from_directory, render_template
from flask import make_response
from flask import request
from flask import Response
from instance import config

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


@app.route('/json')
def jsonfeed():
    with open('rss.json') as json_data:
        d = json.load(json_data)
    return generate_json(d)


@app.route('/rss')
def rss():
    xml = open("rss.xml", "r")
    return Response(xml, mimetype='text/xml')


@app.route('/log')
def log():
    with open('log.json') as json_data:
        d = json.load(json_data)
    return generate_json(d)


@app.route('/update/<pw>')
def update(pw):

    if pw == config.UPDATEPASSWORD:
        make_rss()
        make_json()
        write_log()
        resp = make_response('UPDATED!', 200)
    else:
        resp = make_response('ERROR', 500)
    return resp


def generate_json(f):
    result = json.dumps(f, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None,
                        indent=True, separators=None, encoding="utf-8", sort_keys=False, default=json_util.default)
    resp = make_response(result)
    if request.headers.get('Accept', '').find('application/json') > -1:
        resp.mimetype = 'application/json'
    else:
        resp.mimetype = 'text/plain'
    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=config.SERVER_PORT, threaded=True, debug=True)
