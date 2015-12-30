import argparse
import syslog
from flask import Flask
from redis import StrictRedis

app = Flask(__name__)

@app.route('/jobs/', methods=['GET', 'POST'])
def jobs(job=None):
    return "Get job descriptions here."

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="jobber api server")
    parser.add_argument("-p", "--port", help='The jobber server will listen on this port', default=5000)
    parser.add_argument("-i", "--iface", help='The jobber server will bind to this interface', default="127.0.0.1")
    parser.add_argument("-d", "--debug", help='Start the server in debug mode', action="store_true")
    args = parser.parse_args()
    
    syslog.openlog("jobber service", 0, syslog.LOG_LOCAL0)
    syslog.syslog(syslog.LOG_INFO, "jobber service API starting on {}:{}".format(args.iface, args.port))

    try:
        rd = StrictRedis(host='localhost', port=6379)
    except Exception as e:
        syslog.syslog(syslog.LOG_ERR, "failed to create redis interface: {}".format(e))
    else:
        if args.debug:
            app.debug = True
        app.run(host=args.iface, port=args.port)
    finally:
        syslog.syslog(syslog.LOG_INFO, "jobber service API shutting down")
        syslog.closelog()
