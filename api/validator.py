import json
from jsonschema.exceptions import ValidationError
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
    "description":"A test job definition",
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
            {"hostPath":"/tmp/test-job", "containerPath":"/tmp"},
            {"hostPath":"/var/log/test-job", "containerPath":"/var/log"}
        ],
        "links": [
            {"linkContainer":"LINKCNTR1", "linkName":"LINKCNTR1"},
            {"linkContainer":"LINKCNTR2", "linkName":"LINKCNTR2"}
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

def _format_field_path(absolute_path):
    path = []
    for part in absolute_path:
        if type(part) in [unicode, str]:
            path.append(part)
        elif type(part) is int:
            path[-1] = path[-1] + "[{}]".format(part)
    return '.'.join(path)

try:
    validate_object(spec, job_spec, job_dict)
except Exception as e:
    if type(e) is ValidationError:
        print "Validation failed"
        print "Field: {}".format(_format_field_path(e.absolute_path))
        print "Error: {}".format(e.message)
    else:
        print "Exception of type {}:".format(type(e))
        print e
