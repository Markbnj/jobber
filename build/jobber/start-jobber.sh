#!/bin/bash

debug=false

function help {
    echo "Starts the jobber services inside the container, optionally enabling"
    echo "interactive debugging."
    echo
    echo "Usage: `basename $0` [-h] [-d]"
    echo
    echo "Options:"
    printf "\t-h\t\tShow this help message\n"
    printf "\t-d\tStart the services in debug mode.\n"
    if [ -z "$1" ]; then
        exit 1
    else
        exit $1
    fi
}

while getopts hd opt; do
    case $opt in
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
    /bin/bash
else
    # run the services in production mode
    logger -t 'jobber startup' -p local0.info "jobber services starting in production mode"
    /usr/local/bin/supervisord -n -c /etc/supervisord.conf
fi
