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
CORS(app, resources={f'{route}*': {'origins': ['http://142.93.35.88', 'https://142.93.35.88', 'http://lectiotime.xyz', 'https://lectiotime.xyz']}})

api.add_resource(Meta, '/')

@app.route(f'{route}skema')
def skema_endpoint():
    school_id = request.args.get('school_id', None)
    elev_id = request.args.get('elev_id', None)
    name = request.args.get('name', None)

    if not school_id or not (elev_id or name):
        return 'Missing either school_id, elev_id or name'

    sched = getSchedule(elev_id, school_id)
    print(sched.json())
    return jsonify(sched.json())

@app.route(f'{route}today')
def today_endpoint():
    school_id = request.args.get('school_id', None)
    elev_id = request.args.get('elev_id', None)
    name = request.args.get('name', None)

    if not school_id or not (elev_id or name):
        return 'Missing either school_id, elev_id or name'
    try:
        sched = getSchedule(elev_id, school_id, offset=timedelta(days=0, hours=0))
    except Exception:
        return jsonify({"error": "error"})

    return jsonify(sched.jsonToday())


if __name__ == '__main__':
    app.run()