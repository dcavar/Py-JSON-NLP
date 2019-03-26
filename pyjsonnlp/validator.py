"""
validator.py

(C) 2019 Oren Baldinger, Damir Cavar

Validates the results of pipelines against the NLP-JSON schema.
"""


import json
from collections import OrderedDict
from os.path import realpath, dirname, join

from pyjsonnlp.pipeline import Pipeline
from jsonschema import Draft7Validator, ValidationError
from pyjsonnlp import remove_empty_fields


validator = None


def load_validator() -> Draft7Validator:
    """
    Keep a single validator instance in memory
    :return: The Draft 7 validator
    """
    global validator

    if not validator:
        with open(join(dirname(realpath(__file__)), 'JSON-NLP.schema.json'), 'r') as f:
            validator = Draft7Validator(json.load(f))
    return validator


def is_valid(nlpjson: OrderedDict) -> bool:
    """
    Validates a json-nlp ordered dictionary.
    :param nlpjson: The json-nlp to be validated
    :return: True if the json-nlp validates, False otherwise
    """
    valid = True
    v = load_validator()
    for error in sorted(v.iter_errors(remove_empty_fields(nlpjson)), key=str):
        print(format_error(error))
        valid = False
    return valid


def validate_pipeline(pipeline: Pipeline, text: str) -> bool:
    """
    Validate a Pipeline with a given text, lang, and any other options.
    :param pipeline: The Pipeline to validate
    :param text: String text to validate
    :return: True if the Pipeline validates, False otherwise
    """
    return is_valid(pipeline.process(text=text))


def format_error(error: ValidationError) -> str:
    """
    Formats validation errors as strings
    :param error: The validation error to validate
    :return: String representation of the error
    """
    return f"{error.message} in {', '.join(map(str, error.path))}"

