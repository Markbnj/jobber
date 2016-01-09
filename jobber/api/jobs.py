import syslog
import json
from redis import StrictRedis
from crontabs import add_job, remove_job, sync_jobs
from api_error import BadRequestError, NotFoundError, InternalError
from validator import validate_job


REDIS_HOST = 'localhost'
REDIS_PORT = 6379


def add_job(job):
    validate_job(job)
    rd = _get_redis()

    # hash the name
    # assert that the hash is not in redis
    # if it is throw BadRequestError with relevant msg
    # insert job into redis at hash/key
    # add job to crontab
    return job


def get_jobs(start_pos=None, item_count=None):
    rd = _get_redis()
    # read and deserialize the list of jobs from redis
    # optionally offset to start_pos
    # read either to end or item_count, whichever comes first
    # return resulting subset
    return {"start_pos":start_pos,"item_count":item_count}


def job_results(job_id=None, start_time=None, end_time=None, start_pos=None, item_count=None):
    rd = _get_redis()
    # read and deserialize the job results from redis
    # optionally filter on job_id
    # optionally take the paged subject
    # build and return the paged job results object
    return {"job_id":job_id,"start_time":start_time,"end_time":end_time,"start_pos":start_pos,"item_count":item_count}


def get_job(job_id):
    rd = _get_redis()
    # read and deserialize the job from redis
    # if the key is None raise BadRequestError
    # if the key isn't found raise NotFoundError
    return {"job_id":job_id}


def delete_job(job_id):
    rd = _get_redis()
    # if the key is None raise BadRequestError
    # remove the key from redis
    # if the key isn't found raise NotFoundError
    return {"job_id":job_id}


def update_job(job_id, job):
    validate_job(job)
    rd = _get_redis()
    # assert that the key is in redis
    # if it isn't raise NotFoundError
    # validate the job
    # upsert job into redis at hash/key
    # update the crontab
    return job


def _get_redis():
    try:
        return StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    except Exception as e:
        syslog.syslog(syslog.LOG_ERR, "{}".format(e))
        raise InternalError("Failed to create database interface")
