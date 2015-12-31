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
    # validate the job
    # hash the name
    # assert that the hash is not in redis
    # if it is throw BadRequestError with relevant msg
    # insert job into redis at hash/key
    # add job to crontab
    return job

def get_jobs(start_pos=None, item_count=None):
    # read and deserialize the list of jobs from redis
    # optionally offset to start_pos
    # read either to end or item_count, whichever comes first
    # return resulting subset
    return {'start_pos':start_pos,'item_count':item_count}
    pass