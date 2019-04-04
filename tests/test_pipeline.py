from collections import OrderedDict
from unittest import TestCase

import pytest

from pyjsonnlp.pipeline import Pipeline
from tests.mocks import MockPipeline


class TestPipeline(TestCase):
    def test_process(self):
        pipe = Pipeline()
        with pytest.raises(NotImplementedError):
            pipe.process('some text')

    def test_mock(self):
        assert isinstance(MockPipeline.process(), OrderedDict)
