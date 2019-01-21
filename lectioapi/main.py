from datetime import datetime, timedelta

from flask import Flask, jsonify
from flask_restful import Resource, Api, request
from flask_cors import CORS
from lectio import getSchedule, exists


class Meta(Resource):
    def get(self):
        return request.args


route = '/'
app = Flask(__name__)
api = Api(app)
CORS(app, resources={f'{route}*': {'origins': ['http://142.93.35.88',
                                               'https://142.93.35.88',
                                               'http://lectiotime.xyz',
                                               'https://lectiotime.xyz',
                                               'http://127.0.0.1:5500']}
                    })

api.add_resource(Meta, '/')


@app.route(f'{route}skema')
def skema_endpoint():
    school_id = request.args.get('school_id', None)
    elev_id = request.args.get('elev_id', None)

    if not school_id or not elev_id:
        return 'Missing either school_id or elev_id'

    sched = getSchedule(elev_id, school_id)
    print(sched.json())
    return jsonify(sched.json())


@app.route(f'{route}today')
def today_endpoint():
    school_id = request.args.get('school_id', None)
    elev_id = request.args.get('elev_id', None)

    if not school_id or not elev_id:
        return 'Missing either school_id or elev_id'

    try:
        sched = getSchedule(elev_id, school_id,
                            offset=timedelta(days=0, hours=0))
    except Exception:
        return jsonify({"error": "error"})

    return jsonify(sched.jsonToday())


@app.route(f'{route}exists')
def exists_endpoint():
    school_id = request.args.get('school_id', None)
    elev_id = request.args.get('elev_id', None)

    if not school_id or not elev_id:
        return 'Missing either school_id or elev_id'

    return jsonify({"exists": exists(elev_id, school_id)})


if __name__ == '__main__':
    app.run()
