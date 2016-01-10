"""
.. module:: jobber.api.api_error.py
   :platform: Unix
   :synopsis: Provides three error types used to signal from the CRUD layer to the handlers.

.. moduleauthor:: Mark Betz <betz.mark@gmail.com>


"""
class BadRequestError(Exception):
    pass


class NotFoundError(Exception):
    pass


class InternalError(Exception):
    pass
