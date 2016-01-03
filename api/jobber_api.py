import argparse
import syslog
import json
from flask import Flask, request, make_response
from jobs import add_job, get_jobs, job_results, get_job, delete_job, update_job
from jobs import BadRequestError, NotFoundError, InternalError


app = Flask(__name__)


def _make_error(status, message):
    error = {}
    error['code'] = status
    error['message'] = message
    error['fields'] = ""
    resp = make_response(json.dumps(error), status)
    resp.headers['Content-Type'] = 'application/json'
    return resp


def _make_response(status=200, response=None):
    resp = make_response(json.dumps(response), status)
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route('/jobs/', methods=['GET', 'POST'])
def get_post_jobs():
    if request.method == 'POST':
        job = request.json
        try:
            return _make_response(response=add_job(job))
        except BadRequestError as e:
            return _make_error(400, e.message)
        except Exception as e:
            return _make_error(500, e.message)
    else:
        start_pos = request.args.get('start_pos', None)
        item_count = request.args.get('item_count', None)
        try:
            return _make_response(response=get_jobs(
                    start_pos=start_pos,
                    item_count=item_count))
        except BadRequestError as e:
            return _make_error(400, e.message)
        except Exception as e:
            return _make_error(500, e.message)


@app.route('/jobs/results/', methods=['GET'])
def get_jobs_results():
    start_time = request.args.get('start_time', None)
    end_time = request.args.get('end_time', None)
    start_pos = request.args.get('start_pos', None)
    item_count = request.args.get('item_count', None)
    try:
        return _make_response(response=job_results(
                job_id=None,
                start_time=start_time, 
                end_time=end_time, 
                start_pos=start_pos, 
                item_count=item_count))
    except BadRequestError as e:
        return _make_error(400, e.message)
    except Exception as e:
        return _make_error(500, e.message)


@app.route('/jobs/<job_id>/', methods=['GET','PUT','DELETE'])
def get_put_delete_job(job_id):
    if request.method == 'DELETE':
        try:
            return _make_response(response=delete_job(job_id))
        except NotFoundError as e:
            return _make_error(404, e.message)
        except BadRequestError as e:
            return _make_error(400, e.message)
        except Exception as e:
            return _make_error(500, e.message)
    elif request.method == 'PUT':
        job = request.json
        try:
            return _make_response(response=update_job(job_id, job))
        except BadRequestError as e:
            return _make_error(400, e.message)
        except Exception as e:
            return _make_error(500, e.message)
    else:
        try:
            return _make_response(response=get_job(job_id))
        except NotFoundError as e:
            return _make_error(404, e.message)
        except BadRequestError as e:
            return _make_error(400, e.message)
        except Exception as e:
            return _make_error(500, e.message)


@app.route('/jobs/<job_id>/results/', methods=['GET'])
def get_job_results(job_id):
    start_time = request.args.get('start_time', None)
    end_time = request.args.get('end_time', None)
    start_pos = request.args.get('start_pos', None)
    item_count = request.args.get('item_count', None)
    try:
        return _make_response(response=job_results(
                job_id=job_id,
                start_time=start_time, 
                end_time=end_time, 
                start_pos=start_pos, 
                item_count=item_count))
    except BadRequestError as e:
        return _make_error(400, e.message)
    except Exception as e:
        return _make_error(500, e.message)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="jobber api service")
    parser.add_argument("-p", "--port", help='The jobber api service will listen on this port', default=5000)
    parser.add_argument("-i", "--iface", help='The jobber api service will bind to this interface', default="127.0.0.1")
    parser.add_argument("-d", "--debug", help='Start the service in debug mode', action="store_true")
    args = parser.parse_args()
    
    syslog.openlog("jobber api service", 0, syslog.LOG_LOCAL0)
    syslog.syslog(syslog.LOG_INFO, "jobber API service starting on {}:{}".format(args.iface, args.port))

    # read all job definitions from redis and validate all crontabs
    # if the job exists but the crontab does not rebuild the crontab
    # if the crontab exists but the job does not remove the crontab
    # if both exist but the crontab schedule doesn't match update the crontab
    if args.debug:
        app.debug = True
    app.run(host=args.iface, port=int(args.port))
    syslog.syslog(syslog.LOG_INFO, "jobber API service shutting down")
    syslog.closelog()
