from unittest import TestCase, mock

from tests.mocks import MockPipeline

from pyjsonnlp.microservices.flask_server import FlaskMicroservice, current_app


class TestFlaskMicroservice(TestCase):
    def setUp(self) -> None:
        self.f = FlaskMicroservice('test', MockPipeline())

    def test_write_text(self):
        pass

    def test_handle_error(self):
        pass

    def test_get_text(self):
        pass

    def test_write_json(self):
        pass

    def test_get_output_format(self):
        pass

    def test_get_args(self):
        pass
        # with current_app.test_client() as c:
        #     r = c.get('/', query_string={'name': 'davidism'})
        #     args = {
        #         'constituents': 'true',
        #         'dependencies': 0,
        #         'arg1': 'False'
        #     }
        #     actual = self.f.get_args()
        #     expected = ''
        #     assert expected == actual, actual

    def test_debug(self):
        pass
