from collections import OrderedDict
from unittest import TestCase

from jsonschema import ValidationError

from pyjsonnlp.pipeline import Pipeline
from pyjsonnlp.validation import format_error, validate_pipeline, is_valid


class TestValidation(TestCase):
    def test_is_valid(self):
        valid, errors = is_valid(OrderedDict())
        assert not valid
        assert len(errors)

    def test_validate_pipeline(self):
        assert not validate_pipeline(MockInvalidPipeline(), '')
        assert validate_pipeline(MockValidPipeline(), '')

    def test_format_error(self):
        assert isinstance(format_error(ValidationError("Error!")), str)


class MockValidPipeline(Pipeline):
    def process(self, text=''):
        return OrderedDict({
            'documents': {
                '1': {
                    'id': '1',
                    'tokenList': {
                        1: {
                            'id': 1,
                            'text': 'Minimum'
                        }
                    }
                }
            }
        })


class MockInvalidPipeline(Pipeline):
    def process(self, text=''):
        return OrderedDict()
