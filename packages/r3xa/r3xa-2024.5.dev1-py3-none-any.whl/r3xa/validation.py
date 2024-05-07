# -*- coding: utf-8 -*-
import jsonschema
from r3xa.utils import get_schema


def make_context_message(error, context_error):
    """
    error.validator_value: [{'$ref': '#/$defs/settings/generic'}, {'$ref': '#/$defs/settings/specimen'}]
    context_error.relative_schema_path: deque([0, 'required'])
    """

    i = list(context_error.relative_schema_path)[0]
    return context_error.message + " of " + error.validator_value[i]["$ref"].replace("#/$defs/", "")


def validate(instance):
    schema = get_schema()

    validator = jsonschema.validators.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=jsonschema.exceptions.relevance)

    if not len(errors):
        print("Valid json file")
        return

    error_messages = []

    for error in errors:
        p = f"{list(error.path)[0]} validation error" if error.path.count(0) else "root validation error"
        error_message = [f"{p}: {error.message}"] + [make_context_message(error, e) for e in error.context]
        error_messages.append("\n\t- ".join(error_message))

    msg = "\n".join([f"- {e}" for e in error_messages])

    raise jsonschema.exceptions.ValidationError(msg)
