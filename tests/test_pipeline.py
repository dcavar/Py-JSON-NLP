from unittest import TestCase

import pytest

from pyjsonnlp.pipeline import Pipeline


class TestPipeline(TestCase):
    def test_process(self):
        pipe = Pipeline()
        with pytest.raises(NotImplementedError):
            pipe.process('some text')
