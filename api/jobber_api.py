import argparse
import syslog
import json
from flask import Flask, request, Response
from jobs import add_job, get_jobs
from jobs import BadRequestError, NotFoundError, InternalError


app = Flask(__name__)


def _make_error(status, message):
    """
    Takes an http status code >= 400 and a message and returns
    a properly formatted error response
    """
    error = {}
    error['code'] = status
    error['message'] = message
    error['fields'] = ""
    resp = Response(json.dumps(error))
    resp.headers['Content-Type'] = 'application/json'
    resp.status = status
    return resp


def _make_response(status, response=None):
    """
    Takes an http status code >=200 and a response in json format
    and returns a properly formatted response object
    """
    resp = Response(response)
    resp.headers['Content-Type'] = 'application/json'
    resp.status = status
    return resp


@app.route('/jobs/', methods=['GET', 'POST'])
def get_post_jobs():
    if request.method == 'POST':
        job = request.json
        try:
            return _make_response("200", add_job(job))
        except BadRequestError as e:
            return _make_error("400", e.message)
        except NotFoundError as e:
            return _make_error("404", e.message)
        except Exception as e:
            return _make_error("500", e.message)
    else:
        start = request.args.get('start_pos', None)
        items = request.args.get('item_count', None)
        try:
            return _make_response("200", get_jobs(start, items))
        except BadRequestError as e:
            return _make_error("400", e.message)
        except NotFoundError as e:
            return _make_error("404", e.message)
        except Exception as e:
            return _make_error("500", e.message)


@app.route('/jobs/results/', methods=['GET'])
def get_jobs_results():
    # querystring: start_time
    # querystring: end_time
    # querystring: start_pos
    # querystring: total_items
    # read and deseralize the job run results
    # build and return PagedJobResults structure as application/json
    return "Get run results for all jobs here.\n"

@app.route('/jobs/<job_id>/', methods=['GET','PUT','DELETE'])
def get_put_delete_job(job_id):
    if request.method == 'DELETE':
        # path: job_id
        # Remove the id/key in the redis job db
        # if the key does not exist...
        #     return 404 not found
        # Remove the crontab
        # return 200 OK
        return "Delete job {} definition here.\n".format(job_id)
    elif request.method == 'PUT':
        # path: job_id
        # body: job definition as application/json
        # deserialize and validate the json request body
        # if validation fails...
        #     return 400 bad request
        # put the request body to the id/key in redis
        # if the key doesn't exist... 
        #     return 404 not found
        # update the crontab if needed
        # return 200 OK
        return "Update job {} definition here.\n".format(job_id)
    else:
        # path: job_id
        # read the job definition from redis at the id/key
        # if the key doesn't exist:
        #     return 404 not found
        # return 200 OK w/job definition as application/json

        return "Get job {} definition here.\n".format(job_id)

@app.route('/jobs/<job_id>/results/', methods=['GET'])
def get_job_results(job_id):
    # path: job_id
    # querystring: start_time
    # querystring: end_time
    # querystring: start_pos
    # querystring: total_items
    # read and deseralize the job run results
    # build and return PagedJobResults structure as application/json
    return "Get run results for job {} here.\n".format(job_id)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="jobber api server")
    parser.add_argument("-p", "--port", help='The jobber server will listen on this port', default=5000)
    parser.add_argument("-i", "--iface", help='The jobber server will bind to this interface', default="127.0.0.1")
    parser.add_argument("-d", "--debug", help='Start the server in debug mode', action="store_true")
    args = parser.parse_args()
    
    syslog.openlog("jobber service", 0, syslog.LOG_LOCAL0)
    syslog.syslog(syslog.LOG_INFO, "jobber service API starting on {}:{}".format(args.iface, int(args.port)))

    # read all job definitions from redis and validate all crontabs
    # if the job exists but the crontab does not rebuild the crontab
    # if the crontab exists but the job does not remove the crontab
    # if both exist but the crontab schedule doesn't match update the crontab
    if args.debug:
        app.debug = True
    app.run(host=args.iface, port=args.port)
    syslog.syslog(syslog.LOG_INFO, "jobber service API shutting down")
    syslog.closelog()
