jobs = """
[{
    "name":"test-job-01",
    "description":"Test job 01 definition",
    "templates": [{
        "name":"jobber-test",
        "image":"markbnj/jobber-testjob",
        "replicas":1,
        "command":"/bin/bash",
        "pullAlways": true,
        "ports": [
            {"port":6000,"hostPort":8000},
            {"port":6001,"hostPort":8001}
        ],
        "env": [
            {"name":"VAR1", "value": "VALUE1"},
            {"name":"VAR2", "value": "VALUE2"}
        ],
        "volumes": [
            {"hostPath":"/tmp/test-job-01", "containerPath":"/tmp"},
            {"hostPath":"/var/log/test-job-01", "containerPath":"/var/log"}
        ],
        "links": [
            {"linkContainer":"LINKCNTR1", "linkName":"LINKCNTR1"},
            {"linkContainer":"LINKCNTR2", "linkName":"LINKCNTR2"}
        ]
    }],
    "schedule": {
        "description":"Every five minutes",
        "minutes":"/5",
        "hours":"*",
        "dayOfMonth":"*",
        "month":"*",
        "dayOfWeek":"*",
        "year":"*"
    }
},
{
    "name":"test-job-02",
    "description":"Test 02 job definition",
    "templates": [{
        "name":"jobber-test",
        "image":"markbnj/jobber-testjob",
        "replicas":1,
        "command":"/bin/bash",
        "pullAlways": true,
        "ports": [
            {"port":6000,"hostPort":8000},
            {"port":6001,"hostPort":8001}
        ],
        "env": [
            {"name":"VAR1", "value": "VALUE1"},
            {"name":"VAR2", "value": "VALUE2"}
        ],
        "volumes": [
            {"hostPath":"/tmp/test-job-02", "containerPath":"/tmp"},
            {"hostPath":"/var/log/test-job-02", "containerPath":"/var/log"}
        ],
        "links": [
            {"linkContainer":"LINKCNTR1", "linkName":"LINKCNTR1"},
            {"linkContainer":"LINKCNTR2", "linkName":"LINKCNTR2"}
        ]
    }],
    "schedule": {
        "description":"every five minutes",
        "minutes":"/5",
        "hours":"*",
        "dayOfMonth":"*",
        "month":"*",
        "dayOfWeek":"*",
        "year":"*"
    }
},
{
    "name":"test-job-03",
    "description":"Test 03 job definition",
    "templates": [{
        "name":"jobber-test",
        "image":"markbnj/jobber-testjob",
        "replicas":1,
        "command":"/bin/bash",
        "pullAlways": true,
        "ports": [
            {"port":6000,"hostPort":8000},
            {"port":6001,"hostPort":8001}
        ],
        "env": [
            {"name":"VAR1", "value": "VALUE1"},
            {"name":"VAR2", "value": "VALUE2"}
        ],
        "volumes": [
            {"hostPath":"/tmp/test-job-03", "containerPath":"/tmp"},
            {"hostPath":"/var/log/test-job-03", "containerPath":"/var/log"}
        ],
        "links": [
            {"linkContainer":"LINKCNTR1", "linkName":"LINKCNTR1"},
            {"linkContainer":"LINKCNTR2", "linkName":"LINKCNTR2"}
        ]
    }],
    "schedule": {
        "description":"every five minutes",
        "minutes":"/5",
        "hours":"*",
        "dayOfMonth":"*",
        "month":"*",
        "dayOfWeek":"*",
        "year":"*"
    }
}]"""
