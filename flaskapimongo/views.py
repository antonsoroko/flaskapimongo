import md5
import dateutil.parser
import dateutil.relativedelta
import json
import time
from flask import jsonify, request, abort, make_response, g
from flaskapimongo import app, mongo
from pymongo.errors import OperationFailure


@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)


@app.route('/')
def index():
    activities_collection = mongo.db.activities
    count = activities_collection.count()
    return 'Flask-api-mongo is running! Total entries is {0}. Rendered in {0}'.format(count ,g.request_time())


@app.route('/get', methods = ['GET'])
def get_activity():
    """Get uid and date args and return json object with visit count for requested uid and date."""
    required_args = ['uid', 'date']
    if not all(x in request.args for x in required_args):
        abort(400)
    result_answer = {}
    try:
        req_uid = int(request.args['uid'])
        req_date = dateutil.parser.parse(request.args['date'])
        #removing time from date if user sent full date format
        start_date = req_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + dateutil.relativedelta.relativedelta(days=+1)
        activities_collection = mongo.db.activities
        count = activities_collection.count(filter={'uid': req_uid, 'date': {"$gte": start_date, "$lt": end_date}})
        #old pymongo style
        #count = activities_collection.find({'uid': req_uid, 'date': {"$gte": start_date, "$lt": end_date}}, fields={'uid': 1, '_id': 0}).count()
    except (KeyError,  ValueError, OperationFailure) as e:
        result_answer['status'] = "FAIL"
        result_answer['error'] = str(e)
        return jsonify(result_answer)
    result_answer['status'] = "OK"
    result_answer['uid'] = req_uid
    result_answer['count'] = count
    result_answer['execution_time'] = g.request_time()
    return jsonify(result_answer)


@app.route('/post', methods = ['POST'])
def post_activity():
    """Writes json object to storage if its md5sum is correct.
    Accepts single json object or array."""
    if not request.json:
        abort(400)
    if not isinstance(request.json, list):
        activities = [request.json]
    else:
        activities = request.json
    result_answer = {}
    activities_collection = mongo.db.activities
    for pos, activity in enumerate(activities):
        try:
            recieved_md5 = activity.pop('md5checksum')
            calculated_md5 = md5.new(json.dumps(activity)).hexdigest()
            if recieved_md5 == calculated_md5:
                activity['uid'] = int(activity['uid'])
                activity['date'] = dateutil.parser.parse(activity['date'])
                activities_collection.insert_one(activity)
                result_answer[pos] = "OK"           
            else:
                result_answer[pos] = "FAIL"
        except (KeyError,  ValueError, OperationFailure) as e:
            result_answer[pos] = "FAIL"
    result_answer['execution_time'] = g.request_time()
    return jsonify(result_answer), 201
