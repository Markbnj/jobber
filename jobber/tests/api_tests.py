"""
.. module:: jobber.tests.api_tests.py
   :platform: Unix
   :synopsis: Implements unit tests for the jobber API.

.. moduleauthor:: Mark Betz <betz.mark@gmail.com>

.. note:: To set up and run these tests use the `make test` makefile target.
   The test methods expect the container to be running at the address in
   os.environ['TEST_HOST'] and os.environ['API_TEST_PORT']


"""
import os
import unittest
import urllib2


TEST_HOST = os.environ.get("TEST_HOST")
API_TEST_PORT = os.environ.get("API_TEST_PORT")
API_TEST_URL = u"http://{}:{}".format(TEST_HOST, API_TEST_PORT)


def test_add_job():
    pass


def test_get_job_by_id():
    pass


def test_get_job_by_name():
    pass


def test_update_job():
    pass


def test_get_jobs_results():
    pass


def test_get_paged_jobs_results():
    pass


def test_get_job_results():
    pass


def test_delete_job():
    pass


def test_add_jobs():
    pass


def test_list_jobs():
    pass


def test_paged_jobs():
    pass
