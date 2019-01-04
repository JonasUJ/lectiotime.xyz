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
CORS(app, resources={f'{route}*': {'origins': 'http://142.93.35.88/lectio'}})

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

    sched = getSchedule(elev_id, school_id, offset=timedelta(days=0))
    today = sched.today()
    try:
        json = {
            "name": sched.name,
            "start": today[0].start,
            "end": today[-1].end
        }
    except IndexError:
        json = {
            "name": sched.name,
            "start": datetime.today(),
            "end": datetime.today()
        }
    for i, p in enumerate(today):
        json[str(i)] = p.json()
    return jsonify(json)


if __name__ == '__main__':
    app.run()