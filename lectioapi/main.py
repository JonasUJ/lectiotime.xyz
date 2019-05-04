from datetime import datetime, timedelta

from flask import Flask, jsonify
from flask_restful import Resource, Api, request
from flask_cors import CORS
from lectio import getSchedule

class Meta(Resource):
    def get(self):
        return request.args

route = '/'
app = Flask(__name__)
api = Api(app)
CORS(app, resources={f'{route}*': {'origins': ['http://142.93.35.88', 'https://142.93.35.88', 'http://lectiotime.xyz', 'https://lectiotime.xyz', 'http://127.0.0.1:5500']}})

api.add_resource(Meta, '/')

@app.route(f'{route}skema', methods=['GET', 'POST'])
def skema_endpoint():
    schoolid = request.args.get('schoolid', None)
    user = request.args.get('user', None)
    pwd = request.args.get('pwd', None)

    if not schoolid or not user or not pwd:
        return 'Missing either schoolid, user or pwd'

    sched = getSchedule(schoolid, user, pwd)
    return jsonify(sched.json())

@app.route(f'{route}today', methods=['GET', 'POST'])
def today_endpoint():
    schoolid = request.args.get('schoolid', None)
    user = request.args.get('user', None)
    pwd = request.args.get('pwd', None)

    if not schoolid or not user or not pwd:
        return 'Missing either schoolid, user or pwd'

    sched = getSchedule(schoolid, user, pwd)
    return jsonify(sched.jsonToday())

@app.route(f'{route}start', methods=['GET', 'POST'])
def start_endpoint():
    schoolid = request.args.get('schoolid', None)
    user = request.args.get('user', None)
    pwd = request.args.get('pwd', None)

    if not schoolid or not user or not pwd:
        return 'Missing either schoolid, user or pwd'

    sched = getSchedule(schoolid, user, pwd)
    json = sched.jsonToday()
    return f'{("0" + str(json["start"].hour))[-2:]}:{("0" + str(json["start"].minute))[-2:]}'

@app.route(f'{route}curtime', methods=['GET', 'POST'])
def curtime_endpoint():
    dtn = datetime.now() + timedelta(hours=2)
    return f'{dtn.hour}:{dtn.minute}'

if __name__ == '__main__':
    app.run()
