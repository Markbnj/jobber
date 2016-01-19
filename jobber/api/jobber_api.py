"""
.. module:: jobber.api.jobber_api.py
   :platform: Unix
   :synopsis: Implements the flask app and request handlers for the jobber api.

.. moduleauthor:: Mark Betz <betz.mark@gmail.com>


"""
import argparse
import syslog
import json
import jobs
import api_error
import config
import validator
import tests
from flask import Flask, request, make_response


app = Flask(__name__)


def _make_error(status=500, message=None):
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


@app.route('/swagger/', methods=['GET'])
def get_swagger():
    """ Request handler for the / path.

    GET:  returns the jobber API spec as a swagger json doc.
    Args:
        None

    Returns:
        Swagger spec (str):  jobber swagger spec as json doc.
    """
    try:
        return _make_response(response=validator.get_swagger_spec())
    except Exception as e:
        return _make_error(500, e.message)


@app.route('/settings/', methods=['GET'])
def get_settings():
    """ Request handler for the /settings/ path.

    GET:  returns the current jobber settings as a json doc.
    Args:
        None

    Returns:
        Jobber settings (str):  jobber settings as json doc.
    """
    try:
        return _make_response(response=config.get_settings())
    except Exception as e:
        return _make_error(500, e.message)


@app.route('/postman/', methods=['GET'])
def get_postman():
    """ Request handler for the /postman/ path.

    GET:  returns a postman collection for the API endpoints.
    Args:
        None

    Returns:
        Postman collection (str):  postman collection as json doc.
    """
    try:
        return _make_response(response=tests.get_postman_coll())
    except Exception as e:
        return _make_error(500, e.message)


@app.route('/jobs/', methods=['GET', 'POST'])
def get_post_jobs():
    """ Request handler for /jobs/ path.

    GET:  returns the list of scheduled Jobs
    Args:
        None

    Returns:
        PagedJobs (str):  A list of Jobs with paging metadata as json

    POST:  adds one or more scheduled Jobs to the jobs list
    Args:
        jobs (list):  the Jobs to be added as a list

    Returns:
        Job Ids (list) : new job ids in received order if response status >= 200 and <=499
        Error (str):  json error if response status >=500
    """
    if request.method == 'POST':
        jobs_data = request.json
        try:
            return _make_response(response=jobs.add_jobs(jobs_data))
        except api_error.BadRequestError as e:
            return _make_error(400, e.message)
        except Exception as e:
            return _make_error(500, e.message)
    else:
        start_pos = request.args.get('start_pos', None)
        item_count = request.args.get('item_count', None)
        name = request.args.get('name', None)
        try:
            return _make_response(response=jobs.get_jobs(
                    start_pos=start_pos,
                    item_count=item_count,
                    name=name))
        except api_error.BadRequestError as e:
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
        return _make_response(response=jobs.job_results(
                job_id=None,
                start_time=start_time,
                end_time=end_time,
                start_pos=start_pos,
                item_count=item_count))
    except api_error.BadRequestError as e:
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
            return _make_response(response=jobs.delete_job(job_id))
        except api_error.NotFoundError as e:
            return _make_error(404, e.message)
        except api_error.BadRequestError as e:
            return _make_error(400, e.message)
        except Exception as e:
            return _make_error(500, e.message)
    elif request.method == 'PUT':
        job = request.json
        try:
            return _make_response(response=jobs.update_job(job_id, job))
        except api_error.BadRequestError as e:
            return _make_error(400, e.message)
        except Exception as e:
            return _make_error(500, e.message)
    else:
        try:
            return _make_response(response=jobs.get_job(job_id))
        except api_error.NotFoundError as e:
            return _make_error(404, e.message)
        except api_error.BadRequestError as e:
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
        return _make_response(response=jobs.job_results(
                job_id=job_id,
                start_time=start_time,
                end_time=end_time,
                start_pos=start_pos,
                item_count=item_count))
    except api_error.BadRequestError as e:
        return _make_error(400, e.message)
    except Exception as e:
        return _make_error(500, e.message)


""" API service process.

Args:
    -d:  run the server in debugging mode

"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="jobber api service")
    parser.add_argument("-d", "--debug", help='Start the service in debug mode', action="store_true")
    args = parser.parse_args()
    port = config.SERVICE_PORT
    interface = config.IFACE
    syslog.openlog("jobber api service", 0, syslog.LOG_LOCAL0)
    syslog.syslog(syslog.LOG_INFO, "jobber API service starting on {}:{}".format(interface, port))
    if args.debug:
        app.debug = True
    app.run(host=interface, port=port)
    syslog.syslog(syslog.LOG_INFO, "jobber API service shutting down")
    syslog.closelog()
