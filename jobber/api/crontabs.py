"""
.. module:: jobber.api.crontabs.py
   :platform: Unix
   :synopsis: Uses the python-crontab package to provide CRUD for Job crons.

.. moduleauthor:: Mark Betz <betz.mark@gmail.com>


"""
from crontab import CronTab


def add_job_crontab(job):
    # add the passed job to the crontab list
    pass


def remove_job_crontab(job_id):
    # remove a job from the crontab list by id
    pass


def sync_all_crontabs(jobs):
    # sync the crontab list with the passed job list
    pass