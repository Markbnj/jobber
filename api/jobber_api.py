import argparse
import syslog
from flask import Flask, request
from redis import StrictRedis

app = Flask(__name__)

@app.route('/jobs/', methods=['GET', 'POST'])
def get_post_jobs():
    if request.method == 'POST':
        # body: job definition as application/json
        # deserialize and validate the json request body
        # if validation fails...
        #     return 400 bad request
        # hash the job name
        # reserialize the definition to json, insert into redis w/hash as key
        # if key already exists...
        #     return 400 bad request, message: "Job name already exists"
        # build the cron tab
        # return 200 OK
        return "Post a new job definition here.\n"
    else:
        # querystring: start_pos
        # querystring: item_count
        # read and deserialize all the job definitions
        # select subset if applicable
        # build and return PagedJobs structure as application/json
        return "Get a list of job definitions here.\n"

@app.route('jobs/results/', methods=['GET'])
def get_jobs_results():
    # querystring: start_time
    # querystring: end_time
    # querystring: start_pos
    # querystring: total_items
    # read and deseralize the job run results
    # build and return PagedJobResults structure as application/json
    return "Get run results for all jobs here.\n"

@app.route('jobs/<job_id>/', methods=['GET','PUT','DELETE'])
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

@app.route('jobs/<job_id>/results/', methods=['GET'])
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
    syslog.syslog(syslog.LOG_INFO, "jobber service API starting on {}:{}".format(args.iface, args.port))

    try:
        rd = StrictRedis(host='localhost', port=6379)
    except Exception as e:
        syslog.syslog(syslog.LOG_ERR, "failed to create redis interface: {}".format(e))
    else:
        # read all job definitions from redis and validate all crontabs
        # if the job exists but the crontab does not rebuild the crontab
        # if the crontab exists but the job does not remove the crontab
        # if both exist but the crontab schedule doesn't match update the crontab
        if args.debug:
            app.debug = True
        app.run(host=args.iface, port=args.port)
    finally:
        syslog.syslog(syslog.LOG_INFO, "jobber service API shutting down")
        syslog.closelog()
