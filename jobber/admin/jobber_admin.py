import argparse
import syslog
import json
from flask import Flask, request, Response
import config


app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_home():
    return "Not implemented"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="jobber admin service")
    parser.add_argument("-d", "--debug", help='Start the service in debug mode', action="store_true")
    args = parser.parse_args()
    interface = config.IFACE
    port = config.ADMIN_PORT
    syslog.openlog("jobber admin service", 0, syslog.LOG_LOCAL0)
    syslog.syslog(syslog.LOG_INFO, "jobber admin service starting on {}:{}".format(interface, port))

    if args.debug:
        app.debug = True
    app.run(host=interface, port=port)
    syslog.syslog(syslog.LOG_INFO, "jobber admin service shutting down")
    syslog.closelog()
