"""
.. module:: jobber_api.py
   :platform: Unix
   :synopsis: Implements the flask app and request handlers for the jobber api.

.. moduleauthor:: Mark Betz <betz.mark@gmail.com>


"""
import argparse
import syslog
import json
from flask import Flask, request, make_response
from jobs import add_job, get_jobs, job_results, get_job, delete_job, update_job
from api_error import BadRequestError, NotFoundError, InternalError


app = Flask(__name__)


def _make_error(status=500, message):
    """ Utility method used to create an error response.

    Args:
        status (int):  The http status code to return.
        message (str):  A message to include with the response.

    Returns:
        Error (str):  The error information in json format.
    """
    error = {}
    error['code'] = status
    error['message'] = message
    error['fields'] = ""
    resp = make_response(json.dumps(error), status)
    resp.headers['Content-Type'] = 'application/json'
    return resp


def _make_response(status=200, response=None):
    """ Utility method used to create a successful response.

    Args:
        status (int):  The http status code to return.
        response (dict):  The response data as a python dict.

    Returns:
        response (dict):  The completed response object.
    """
    resp = make_response(json.dumps(response), status)
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route('/jobs/', methods=['GET', 'POST'])
def get_post_jobs():
    """ Request handler for /jobs/ path.
    
    GET:  returns the list of scheduled Jobs
    Args:
        None

    Returns:
        PagedJobs (str):  A list of Jobs with paging metadata as json

    POST:  adds a scheduled Job to the jobs list
    Args:
        job (str):  the Job to be added as json

    Returns:
        Nothing : if response status >= 200 and <=499
        Error (str):  json error if response status >=500
    """
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
    """ Request handler for /jobs/results path.

    GET:  returns a list of results for all scheduled jobs
    Args:
        start_time (datetime):  filter results older than the passed datetime
        end_time (datetime):  filter results younger than the passed datetime
        start_pos (int):  start returning results at this ordinal position
        item_count (int):  return this many results

    Returns:
        PagedJobResults (str):  paged list of job results if response status == 200.
        Error (str):  json error if response status >= 500
    """
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
    """ Request handler for the /jobs/<job_id> path.

    GET:  returns the record for a specific job by id.
    Args:
        job_id (str):  the unique identifier of the job.

    Returns:
        Job (str):  job record as json if response status == 200.
        Error (str):  json error if response status >= 500

    PUT:  amends the record for a specific job by id.
    Args:
        job_id (str):  the unique identifier of the job.

    Body:
        job:  job data in json format.
    
    Returns:
        Nothing:  if response status >= 200 and <= 499.
        Error (str):  json error if response status >= 500

    DELETE:  removes the record for a specific job by id.
    Args:
        job_id (str):  the unique identifier of the job.

    Returns:
        Nothing:  if response status >= 200 and <= 499.
        Error (str):  json error if response status >= 500
    """
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
    """ Request handler for the /jobs/<job_id>/results path.

    GET:
    Args:
        start_time (datetime):  filter results older than the passed datetime
        end_time (datetime):  filter results younger than the passed datetime
        start_pos (int):  start returning results at this ordinal position
        item_count (int):  return this many results

    Returns:
        PagedJobResults (str):  paged list of job results if response status == 200.
        Error (str):  json error if response status >= 500
    """
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
