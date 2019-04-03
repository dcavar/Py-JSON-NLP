import json
import logging
from collections import OrderedDict

from flask import Flask, request, current_app, Response

from pyjsonnlp.microservices import Microservice
from pyjsonnlp.pipeline import Pipeline

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class FlaskMicroservice(Microservice, Flask):
    def __init__(self, import_name, pipeline: Pipeline, base_route='/'):
        Microservice.__init__(self, pipeline, base_route)
        Flask.__init__(self, import_name)

        self.add_url_rule(base_route, view_func=self.process)
        self.add_url_rule(base_route + 'dependencies', view_func=self.dependencies)
        self.add_url_rule(base_route + 'constituents', view_func=self.constituents)
        self.add_url_rule(base_route + 'token_list', view_func=self.token_list)
        self.add_url_rule(base_route + 'coreferences', view_func=self.coreferences)
        self.add_url_rule(base_route + 'expressions', view_func=self.expressions)

    def write_text(self, conll: str):
        """Write CONLLU format to the response."""
        return Response(conll, mimetype='text/plain')

    def handle_error(self, error: Exception):
        logger.exception(error)
        return Response(json.dumps({'error': str(error)}), mimetype=current_app.config['JSONIFY_MIMETYPE'], status=500)

    def get_text(self) -> str:  # , upload_folder: str
        """Check the input for text to parse, and return it."""
        if request.method == 'GET':
            if request.args.get('url'):
                return self.scrape_website(request.args.get('url'))
            if request.args.get('text'):
                return request.args.get('text')
            raise NotImplementedError('You need to provide data to parse!')  # todo redirect to help page
        if request.is_json:
            data = request.get_json()
            if 'text' not in data:
                raise NotImplementedError('You need to provide data to parse!')
            return data.get('text')
        if 'text' in request.form:
            return request.form['text']
        if 'url' in request.form:
            return self.scrape_website(request.form['url'])

        raise NotImplementedError('You need to provide data to parse!')

    def write_json(self, j: OrderedDict):
        """Preserves the order of the json object"""
        return current_app.response_class(
            json.dumps(j, indent=2, separators=(', ', ': ')) + '\n',
            mimetype=current_app.config['JSONIFY_MIMETYPE']
        )

    def get_output_format(self):
        return request.args.get('format', 'jsonnlp')

    def get_args(self) -> dict:
        return dict(request.args)

    def debug(self):
        self.run(debug=True)
