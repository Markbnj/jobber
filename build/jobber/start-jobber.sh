#!/bin/bash

debug=false
iface=${IFACE}
port=${PORT}
admin_port=${ADMIN_PORT}

function help {
    echo "Starts the jobber services inside the container, optionally enabling"
    echo "interactive debugging."
    echo 
    echo "Usage: `basename $0` [-h] [-d] [-i IFACE] [-p PORT] [-a ADMIN_PORT]"
    echo
    echo "Options:"
    printf "\t-h\t\tShow this help message\n"
    printf "\t-d\tStart the services in debug mode.\n"
    printf "\t-i <IFACE>\tInterface to bind the services to (defaults to localhost).\n"
    printf "\t-p <PORT>\tAPI services port (defaults to 5000).\n"
    printf "\t-a <ADMIN_PORT>\tAdmin services port (defaults to 8080).\n"
    if [ -z "$1" ]; then
        exit 1
    else
        exit $1
    fi
}

while getopts hdi:p:a: opt; do
    case $opt in
        a)
            admin_port=$OPTARG
            ;;
        p)
            port=$OPTARG
            ;;
        i)
            iface=$OPTARG
            ;;
        d)
            debug=true
            ;;
        h)
            help
            ;;
        *)
            echo "ERROR: Unknown option ${opt}"
            help 1
            ;;
    esac
done

service rsyslog start
export PYTHONPATH=${PYTHONPATH}"/usr/local/bin/jobber"
if $debug; then
    # run the services in debug mode
    logger -t 'jobber startup' -p local0.info "jobber services starting in debug mode"
    /usr/local/bin/supervisord -c /etc/supervisord.debug.conf
    echo "Jobber container started in debug mode"
    echo "Use ./debug-api to start the API services interactively (ctrl-c to exit)"
    echo "Use ./debug-admin to start the admin services interactively (ctrl-c to exit)"
    cd /usr/local/bin/jobber
else
    # run the services in production mode
    logger -t 'jobber startup' -p local0.info "jobber services starting in production mode"
    /usr/local/bin/supervisord -c /etc/supervisord.conf
fi
/bin/bash