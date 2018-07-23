import os
from flask import Flask, abort
from flask import request
from app.call_handler import CallHandler
from app.call import Call
from app.respondent import Respondent
import json

call_handler = CallHandler()
app = Flask(__name__)


@app.route('/')
def index():
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/call-center/api/v1.0/add_respondent', methods=['POST'])
def add_respondent():
    if not request.json:
        abort(400)
    print(request)
    respondent_type = request.json["respondent_type"]
    if respondent_type == 'respondent':
        Respondent(call_handler, 'respondent')
    elif respondent_type == 'manager':
        Respondent(call_handler, 'manager')
    else:
        Respondent(call_handler, 'director')
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/call-center/api/v1.0/make_call', methods=['GET'])
def make_call():
    if not call_handler.dispatch_call(Call(call_handler)):
        return json.dumps({'success': False}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/call-center/api/v1.0/complete_call', methods=['GET'])
def complete_call():
    available_respondents = list(filter(lambda x: not x.is_free(), call_handler.respondents))
    if len(available_respondents) > 0:
        available_respondents[0].complete_call()
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'success': False}), 200, {'ContentType': 'application/json'}


@app.route('/call-center/api/v1.0/status', methods=['GET'])
def status():
    available_respondents = [{"rank": x.rank, "is_free": x.is_free()} for x in call_handler.respondents]
    print(available_respondents)
    return json.dumps({'output': available_respondents}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    if os.environ['ENVIRONMENT'] == 'production':
        app.run(port=80,host='0.0.0.0')
    if os.environ['ENVIRONMENT'] == 'local':
        app.run(port=5000,host='0.0.0.0')