import os
import json
from jsonschema.exceptions import ValidationError
from bravado_core.spec import Spec
from bravado_core.validate import validate_object
from api_error import BadRequestError, NotFoundError, InternalError


bravado_config = {
    'validate_swagger_spec': False,
    'validate_requests': False,
    'validate_responses': False,
    'use_models': True,
}


dir_path = os.path.dirname(os.path.abspath(__file__))
spec_path = os.path.join(dir_path, "swagger/swagger-spec.json")
spec_dict = json.loads(open(spec_path,'r').read())
spec = Spec.from_dict(spec_dict, config=bravado_config)
Job = spec_dict['definitions']['Job']


def _format_field_path(absolute_path):
    path = []
    for part in absolute_path:
        if type(part) in [unicode, str]:
            path.append(part)
        elif type(part) is int:
            path[-1] = path[-1] + "[{}]".format(part)
    return '.'.join(path)


def validate_job(job):
    try:
        validate_object(spec, Job, job)
    except ValidationError as e:
        message = "Invalid job definition:\n Field: {}\n Error: {}".format(_format_field_path(e.absolute_path),e.message)
        raise BadRequestError(message)