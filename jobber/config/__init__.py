"""
.. module:: config.__init__.py
   :platform: Unix
   :synopsis: Defines global settings and imports overrides from the
    environment and any config file.

.. moduleauthor:: Mark Betz <betz.mark@gmail.com>


"""
import os
import yaml


# Port that the API service will listen on
SERVICE_PORT = 5000


# Port that the admin web service will listen on
ADMIN_PORT = 8080


# Interface that both the API and admin service will bind to
IFACE = '127.0.0.1'


# Where the config module will look for values to override these
# settings
CONFIG_PATH = u'/etc/jobber/jobber.yml'


# Where job definition files will be loaded from. Each path is
# checked for any .yaml or .json files containing jobs. A path
# may be a url, in which case a json response is expected.
JOB_PATHS = [u'/etc/jobber/conf.d/']


# How often to sync crontabs and the database, in seconds
SYNC_CRONTABS_SECS = 60


# Path where jobber API and admin services will write logs
LOG_PATH = u'/var/log/jobber/'


# The name of the log to which both services will write
LOG_NAME = u'jobber.log'


# If non-zero, then maximum size of a log before rotation
LOG_MAX_SIZE = 0


# If non-zero, and LOG_MAX_SIZE is set, the maximum number
# of logs to retain.
LOG_MAX_LOGS = 0


# The path to which job logs will be written.
JOB_LOG_PATH = u'/var/log/jobber/'


def import_environment():
    SERVICE_PORT = os.environ.get('SERVICE_PORT', SERVICE_PORT)
    ADMIN_PORT = os.environ.get('ADMIN_PORT', ADMIN_PORT)
    IFACE = os.environ.get('IFACE', IFACE)
    JOB_PATHS = os.environ.get('JOB_PATHS', JOB_PATHS)
    SYNC_CRONTABS_SECS = os.environ.get('SYNC_CRONTABS_SECS', SYNC_CRONTABS_SECS)
    LOG_PATH = os.environ.get('LOG_PATH', LOG_PATH)
    LOG_NAME = os.environ.get('LOG_NAME', LOG_NAME)
    LOG_MAX_SIZE = os.environ.get('LOG_MAX_SIZE', LOG_MAX_SIZE)
    LOG_MAX_LOGS = os.environ.get('LOG_MAX_LOGS', LOG_MAX_LOGS)
    JOB_LOG_PATH = os.environ.get('JOB_LOG_PATH', JOB_LOG_PATH)


def import_config_file():
    global CONFIG_PATH 
    CONFIG_PATH = os.environ.get('CONFIG_PATH', CONFIG_PATH)
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as fconfig:
            config = yaml.safe_load(f)
        SERVICE_PORT = config.get('SERVICE_PORT', SERVICE_PORT)
        ADMIN_PORT = config.get('ADMIN_PORT', ADMIN_PORT)
        IFACE = config.get('IFACE', IFACE)
        JOB_PATHS = config.get('JOB_PATHS', JOB_PATHS)
        SYNC_CRONTABS_SECS = config.get('SYNC_CRONTABS_SECS', SYNC_CRONTABS_SECS)
        LOG_PATH = config.get('LOG_PATH', LOG_PATH)
        LOG_NAME = config.get('LOG_NAME', LOG_NAME)
        LOG_MAX_SIZE = config.get('LOG_MAX_SIZE', LOG_MAX_SIZE)
        LOG_MAX_LOGS = config.get('LOG_MAX_LOGS', LOG_MAX_LOGS)
        JOB_LOG_PATH = config.get('JOB_LOG_PATH', JOB_LOG_PATH)

def get_settings():
    pass    

import_config_file()
import_environment()