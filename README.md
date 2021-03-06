# jobber
A container scheduling job service for kubernetes and docker compose.

##Description

The jobber image runs as a service either on Docker Compose or on the kubernetes container management platform. On startup it checks a configurable path for a json or yaml file listing the jobs to schedule. Jobs are implemented as docker containers that are started, execute some task, and then exit. Jobber exposes a REST API for CRUD on scheduled jobs, as well as cumulative stats on prior job runs (run time, exit code, etc.) Jobs are described to the system by json/yaml definitions either present in the configuration file at startup or added through the REST API. Jobber also exposes a port for recieving log messages from jobs in syslog format, and injects its own address and the log port into job containers when launching them. Jobber can either log received messages to a configurable path, or send them to a remote log sync.

