import syslog
import json
from redis import StrictRedis
from crontabs import add_job, remove_job, sync_jobs

class BadRequestError(Exception):
    pass

class NotFoundError(Exception):
    pass

class InternalError(Exception):
    pass

def _validate_job(job):
    # validate the job
    # raise BadRequestError on fail with relevant msg
    pass

def add_job(job):
    try:
        rd = StrictRedis(host='localhost', port=6379)
    except Exception as e:
        syslog.syslog(syslog.LOG_ERR, "{}".format(e))
        raise InternalError("Failed to create database interface")

    # validate the job
    # hash the name
    # assert that the hash is not in redis
    # if it is throw BadRequestError with relevant msg
    # insert job into redis at hash/key
    # add job to crontab
    return job

def get_jobs(start_pos=None, item_count=None):
    try:
        rd = StrictRedis(host='localhost', port=6379)
    except Exception as e:
        syslog.syslog(syslog.LOG_ERR, "{}".format(e))
        raise InternalError("Failed to create database interface")

    # read and deserialize the list of jobs from redis
    # optionally offset to start_pos
    # read either to end or item_count, whichever comes first
    # return resulting subset
    return {"start_pos":start_pos,"item_count":item_count}

def job_results(job_id=None, start_time=None, end_time=None, start_pos=None, item_count=None):
    try:
        rd = StrictRedis(host='localhost', port=6379)
    except Exception as e:
        syslog.syslog(syslog.LOG_ERR, "{}".format(e))
        raise InternalError("Failed to create database interface")
    # read and deserialize the job results from redis
    # optionally filter on job_id
    # optionally take the paged subject
    # build and return the paged job results object
    return {"job_id":job_id,"start_time":start_time,"end_time":end_time,"start_pos":start_pos,"item_count":item_count}

def get_job(job_id):
    try:
        rd = StrictRedis(host='localhost', port=6379)
    except Exception as e:
        syslog.syslog(syslog.LOG_ERR, "{}".format(e))
        raise InternalError("Failed to create database interface")
    # read and deserialize the job from redis
    # if the key is None raise BadRequestError
    # if the key isn't found raise NotFoundError
    return {"job_id":job_id}

def delete_job(job_id):
    try:
        rd = StrictRedis(host='localhost', port=6379)
    except Exception as e:
        syslog.syslog(syslog.LOG_ERR, "{}".format(e))
        raise InternalError("Failed to create database interface")
    # if the key is None raise BadRequestError
    # remove the key from redis
    # if the key isn't found raise NotFoundError
    return {"job_id":job_id}
