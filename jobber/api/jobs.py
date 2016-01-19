"""
.. module:: jobber.api.jobs.py
   :platform: Unix
   :synopsis: Implements all the core functions for CRUD on Job data.

.. moduleauthor:: Mark Betz <betz.mark@gmail.com>


"""
import syslog
import json
import hashlib
import redis
import crontabs
import api_error
import validator


REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_JOB_DB = 0


# This module should also create a threadworker that syncs the job
# crontabs every config.SYNC_CRONTABS_SECS seconds.


def add_jobs(jobs):
    """ Adds one or more scheduled jobs to the database.

    Args:
        jobs (list):  list of Jobs to be added

    Returns:
        job_ids (list):  list of the resulting job_ids in added order.

    Raises:
        api_error.BadRequestError

    """
    job_ids = []
    rd = _get_redis()
    for job in jobs:
        validator.validate_job(job)
        job_id = hashlib.sha1(job['name']).hexdigest()
        if rd.exists(job_id):
            raise api_error.BadRequestError("Job named {} already exists".format(job['name']))
        rd.set(job_id, json.dumps(job))
        crontabs.add_job(job)
        job_ids.append(job_id)
    return job_ids


def get_jobs(start_pos=None, item_count=None, name=None):
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
    validator.validate_job(job)
    rd = _get_redis()
    # assert that the key is in redis
    # if it isn't raise NotFoundError
    # validate the job
    # upsert job into redis at hash/key
    # update the crontab
    return job


def _get_redis():
    try:
        return redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_JOB_DB)
    except Exception as e:
        syslog.syslog(syslog.LOG_ERR, "{}".format(e))
        raise api_error.InternalError("Failed to create database interface")
