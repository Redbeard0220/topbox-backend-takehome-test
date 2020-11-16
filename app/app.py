from bson import json_util, ObjectId
from flask import Flask
from flask import request
from datetime import datetime


from app.helpers import mongo_client

API_VERSION = '1.0'

app = Flask(__name__)
db = mongo_client()


@app.route('/')
def root():
    response = {'apiVersion': API_VERSION, 'appName': 'Topbox Backend Take Home Test'}
    return json_util.dumps(response)


@app.route('/clients')
def clients():
    return json_util.dumps(db.clients.find({}))


@app.route('/clients/<client_id>')
def clients_by_id(client_id):
    client_object_id = ObjectId(client_id)
    return json_util.dumps(db.clients.find_one({'_id': client_object_id}))


@app.route('/engagements')
def engagements():
    return json_util.dumps(db.engagements.find({}))


@app.route('/engagements/<engagement_id>')
def engagements_by_id(engagement_id):
    engagement_object_id = ObjectId(engagement_id)
    return json_util.dumps(db.engagements.find_one({'_id': engagement_object_id}))


@app.route('/interactions/<engagement_id>')
def interactions(engagement_id):
    # TODO: Modify this endpoint according to problem statement!
    engagement_object_id = ObjectId(engagement_id)
    # verify this is an engagementId which exists
    if db.engagements.find({'_id': engagement_object_id}).count() > 0:
        # set startDate to the beginning of time if it's not in the queryParams
        start = request.args.get('startDate') if 'startDate' in request.args else '1970-01-01T00:00:00'
        # set endDate to the end of time of it's not in the queryParams
        end = request.args.get('endDate') if 'endDate' in request.args else '9999-01-01T00:00:00'

        start_iso = datetime.fromisoformat(start)
        end_iso = datetime.fromisoformat(end)
        query_obj = {
            'engagementId': engagement_object_id,
            'interactionDate': {'$lte': end_iso, '$gte': start_iso}
        }
        return json_util.dumps(db.interactions.find(query_obj))
    # it wasn't an engagementId, so we return search by interaction_id instead
    else:
        return interactions_by_id(engagement_id)


@app.route('/interactions/<interaction_id>')
def interactions_by_id(interaction_id):
    interaction_object_id = ObjectId(interaction_id)
    return json_util.dumps(db.interactions.find_one({'_id': interaction_object_id}))
