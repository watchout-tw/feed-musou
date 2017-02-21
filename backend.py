 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import json
import os
from feed_maker import *
from bson import json_util
from flask import Flask, url_for, send_from_directory, render_template
from flask import make_response
from flask import request
from flask import Response
from instance import config
import datetime
import time

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


@app.route('/json')
def jsonfeed():
    args = request.args
    try:
      d = ''
      if check_token(args):
        with open('rss_full.json') as json_data:
          d = json.load(json_data)
          log_token_using(request.args['token'], request.headers['Cf-Connecting-Ip'])
      else: 
        with open('rss.json') as json_data:
          d = json.load(json_data)
      return generate_json(d)
    except IOError:
      return make_response('ERROR', 500)


@app.route('/rss')
def rss():
    args = request.args
    try:
      xml = ''
      if check_token(args):
        xml = open("rss_full.xml", "r")
        log_token_using(request.args['token'], request.headers['Cf-Connecting-Ip'])
      else:
        xml = open("rss.xml", "r")
      return Response(xml, mimetype='text/xml')
    except IOError:
      return make_response('ERROR', 500)

@app.route('/log')
def log():
    try:
      d = ''
      with open('log.json') as json_data:
        d = json.load(json_data)
      return generate_json(d)
    except IOError:
      return make_response('ERROR', 500)


@app.route('/tokenlog/<pw>')
def tokenlog(pw):
    if pw == config.UPDATEPASSWORD:
      try:
        d = ''
        with open('token_using_log.json') as json_data:
          d = json.load(json_data)
        return generate_json(d)
      except IOError:
        return make_response('ERROR', 500)  
    else:
      resp = make_response('ERROR', 500)
    return resp


@app.route('/update/<pw>')
def update(pw):

    if pw == config.UPDATEPASSWORD:
      make_rss('ABSTRACT')
      make_rss('FULL')
      make_json('ABSTRACT')
      make_json('FULL')
      write_log()
      resp = make_response('UPDATED!', 200)
    else:
      resp = make_response('ERROR', 500)
    return resp


def check_token(args):
  args = request.args
  if 'token' in args:
    for token in config.TOKEN_LIST:
      if token['token'] == args['token']:
        return True
  return False


def log_token_using(token, ip):
  logdata = []
  flag_new_user = 1
  flag_new_ip = 1

  if os.path.isfile('token_using_log.json'):
    with open('token_using_log.json') as json_data:
      print json_data
      logdata = json.load(json_data)
      print logdata
      json_data.close()
    for user in logdata:
      if token == user['token']:
        flag_new_user = 0
        for ipitem in user['ip_list']:
          if ip == ipitem['ip']:
            ipitem['count'] += 1
            ipitem['last_connect_time'] = str(datetime.datetime.now() + datetime.timedelta(hours=8))
            flag_new_ip = 0
            break
        if flag_new_ip == 1:
          user['ip_list'].append(add_token_using_ip(ip))
  else :
    pass
  if flag_new_user == 1:
    logdata.append(add_token_using_user(token,ip))

  with open('token_using_log.json', 'w') as fp:
    json.dump(logdata, fp)
    fp.close()


def add_token_using_ip(ip):
    return {'ip':ip,'count':1,'last_connect_time':str(datetime.datetime.now() + datetime.timedelta(hours=8))}


def add_token_using_user(token,ip):
    return {'token':token,'ip_list':[add_token_using_ip(ip)]}


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
