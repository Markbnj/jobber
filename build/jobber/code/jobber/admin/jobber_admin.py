import argparse
import syslog
import json
from flask import Flask, request, Response


app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_home():
    return "Not implemented"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="jobber admin service")
    parser.add_argument("-p", "--port", help='The jobber admin service will listen on this port', default=8080)
    parser.add_argument("-i", "--iface", help='The jobber admin service will bind to this interface', default="127.0.0.1")
    parser.add_argument("-d", "--debug", help='Start the service in debug mode', action="store_true")
    args = parser.parse_args()
    
    syslog.openlog("jobber admin service", 0, syslog.LOG_LOCAL0)
    syslog.syslog(syslog.LOG_INFO, "jobber admin service starting on {}:{}".format(args.iface, args.port))

    if args.debug:
        app.debug = True
    app.run(host=args.iface, port=int(args.port))
    syslog.syslog(syslog.LOG_INFO, "jobber admin service shutting down")
    syslog.closelog()
