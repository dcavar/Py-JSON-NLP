from collections import OrderedDict
from unittest import TestCase, mock

import pytest

from pyjsonnlp.pipeline import Pipeline, RemotePipeline
from tests.mocks import MockPipeline, MockResponse, MockBadResponse


class TestPipeline(TestCase):
    def test_process(self):
        pipe = Pipeline()
        with pytest.raises(NotImplementedError):
            pipe.process('some text')

    def test_mock(self):
        assert isinstance(MockPipeline.process(), OrderedDict)


class TestRemotePipeline(TestCase):
    def test_url_options(self):
        p = RemotePipeline('www.google.com')
        assert 'http://www.google.com' == p.url, p.url
        p = RemotePipeline('www.google.com/')
        assert 'http://www.google.com' == p.url, p.url
        p = RemotePipeline('https://www.google.com')
        assert 'https://www.google.com' == p.url, p.url
        p = RemotePipeline('localhost', port=9000)
        assert 'http://localhost:9000' == p.url, p.url

    @mock.patch('requests.post')
    def test_process(self, post):
        post.return_value = MockResponse()
        assert isinstance(RemotePipeline('localhost').process(), OrderedDict)

    @mock.patch('requests.post')
    def test_process_error(self, post):
        post.return_value = MockBadResponse()
        pipeline = RemotePipeline('localhost')
        with pytest.raises(BrokenPipeError):
            pipeline.process()
