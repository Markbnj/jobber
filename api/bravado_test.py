import json
from bravado_core.spec import Spec
from bravado_core.validate import validate_object

spec_as_dict = json.loads(open('swagger/swagger-spec.json','r').read())

job_spec = spec_as_dict['definitions']['Job']

config = {
    'validate_swagger_spec': False,
    'validate_requests': False,
    'validate_responses': False,
    'use_models': True,
}

spec = Spec.from_dict(spec_as_dict, config=config)

job_json = """{
    "name":"test-job-01",
    "description":21,
    "templates": [{
        "name":"jobber-test",
        "image":"markbnj/jobber-testjob",
        "replicas":1,
        "command":"/bin/bash",
        "pullAlways": true,
        "ports": [
            {"port":6000,"hostPort":8000,"name":"some fake port"},
            {"port":6001,"hostPort":8001,"name":"another fake port"}
        ],
        "env": [
            {"name: "VAR1", 'value': "VALUE1"},
            {"name: "VAR2", 'value': "VALUE2"}
        ],
        "volumes": [
            {"name":"VOL1", "hostPath":"/tmp/test-job", "containerPath":"/tmp"},
            {"name":"VOL2", "hostPath":"/var/log/test-job", "containerPath":"/var/log"}
        ],
        "links": [
            {"name":"LINK1", "linkContainer":"LINKCNTR1", "linkName":"LINKCNTR1"},
            {"name":"LINK2", "linkContainer":"LINKCNTR2", "linkName":"LINKCNTR2"}
        ]
    }],
    "schedule": {
        "description":"every five minutes",
        "minutes":"5",
        "hours":"*",
        "dayOfMonth":"*",
        "month":"*",
        "dayOfWeek":"*",
        "year":"*"
    }
}"""

job_dict = json.loads(job_json)

validate_object(spec, job_spec, job_dict)
