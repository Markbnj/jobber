"""
.. module:: jobber.api.tests
   :platform: Unix
   :synopsis: Implements unit tests and provides utility methods to get test data.

.. moduleauthor:: Mark Betz <betz.mark@gmail.com>


"""
import os
import json

dir_path = os.path.dirname(os.path.abspath(__file__))
coll_path = os.path.join(dir_path, "postman/jobber_api.postman_collection")

def get_postman_coll():
    with open(coll_path,'r') as coll:
        return json.loads(coll.read())
