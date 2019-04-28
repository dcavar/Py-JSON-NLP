from collections import OrderedDict
from unittest import TestCase, mock

import pytest

from tests.mocks import MockMicroservice, MockPipeline, MockResponse


class TestMicroservice(TestCase):
    def setUp(self) -> None:
        self.ms = MockMicroservice(MockPipeline())

    def test_base_route(self):
        ms = MockMicroservice(MockPipeline(), base_route='/test')
        assert '/test' == ms.route, ms.route

    def test_with_expressions(self):
        assert not self.ms.with_expressions
        assert not self.ms.with_constituents
        assert not self.ms.with_coreferences
        assert not self.ms.with_dependencies
        self.ms.with_expressions = True
        assert self.ms.with_expressions
        assert not self.ms.with_constituents
        assert not self.ms.with_coreferences
        assert not self.ms.with_dependencies

    def test_with_constituents(self):
        assert not self.ms.with_expressions
        assert not self.ms.with_constituents
        assert not self.ms.with_coreferences
        assert not self.ms.with_dependencies
        self.ms.with_constituents = True
        assert not self.ms.with_expressions
        assert self.ms.with_constituents
        assert not self.ms.with_coreferences
        assert not self.ms.with_dependencies

    def test_with_coreferences(self):
        assert not self.ms.with_expressions
        assert not self.ms.with_constituents
        assert not self.ms.with_coreferences
        assert not self.ms.with_dependencies
        self.ms.with_coreferences = True
        assert not self.ms.with_expressions
        assert not self.ms.with_constituents
        assert self.ms.with_coreferences
        assert not self.ms.with_dependencies

    def test_with_dependencies(self):
        assert not self.ms.with_expressions
        assert not self.ms.with_constituents
        assert not self.ms.with_coreferences
        assert not self.ms.with_dependencies
        self.ms.with_dependencies = True
        assert not self.ms.with_expressions
        assert not self.ms.with_constituents
        assert not self.ms.with_coreferences
        assert self.ms.with_dependencies

    def test_run_pipeline(self):
        pass

    # def test_allowed_file(self):
    #     self.ms.allowed_extensions = {'txt'}
    #     assert True is self.ms.allowed_file('/tmp/somefile.txt')
    #     assert True is self.ms.allowed_file('/tmp/somefile.TXT')
    #     assert False is self.ms.allowed_file('/tmp/somefile.jpg')

    def test_check_output_format(self):
        self.ms.allowed_formats = {'conllu', 'jsonnlp'}
        actual = self.ms.check_output_format('jsonnlp')
        assert 'jsonnlp' == actual, actual
        actual = self.ms.check_output_format('CoNLL-U')
        assert 'conllu' == actual, actual
        with pytest.raises(IOError):
            self.ms.check_output_format('xml')

    def test_normalize_language(self):
        pass

    @mock.patch('requests.get')
    def test_scrape_website(self, get):
        get.return_value = MockResponse()
        actual = self.ms.scrape_website('https://docs.python.org/2/tutorial/datastructures.html')
        assert len(actual) > 1, len(actual)

    def test_scrape_website_fail(self):
        with pytest.raises(IOError):
            self.ms.scrape_website('https://sadfsdfdsfsdfsdfsdf.com')

    def test_write_output(self):
        pass

    def test_get_text(self):
        pass

    def test_write_json(self):
        actual = self.ms.write_json(OrderedDict())
        expected = {'mock': 'json'}
        assert expected == actual, actual

    def test_write_text(self):
        pass

    def test_get_output_format(self):
        pass

    def test_get_args(self):
        pass

    def test_handle_error(self):
        pass

    def test_process(self):
        pass

    def test_dependencies(self):
        pass

    def test_constituents(self):
        pass

    def test_token_list(self):
        pass

    def test_coreferences(self):
        pass

    def test_expressions(self):
        pass
