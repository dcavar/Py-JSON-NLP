
from collections import OrderedDict
from enum import Enum

import iso639
import requests
from bs4 import BeautifulSoup

from pyjsonnlp.conversion import to_conllu
from pyjsonnlp.pipeline import Pipeline


class Process(Enum):
    FULL = 1
    DEPS = 2
    COREF = 3
    CONST = 4
    EXPR = 5
    TOKENS = 6


class Microservice(object):
    allowed_extensions = {'txt'}
    allowed_formats = {'jsonnlp', 'conllu'}
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'

    def __init__(self, pipeline: Pipeline, base_route='/'):
        self.pipeline: Pipeline = pipeline

        self.route = base_route

        self.__with_deps = False
        self.__with_coref = False
        self.__with_constituents = False
        self.__with_expressions = False
        self.__with_process_conll = False

    @property
    def with_coreferences(self):
        return self.__with_coref

    @with_coreferences.setter
    def with_coreferences(self, value):
        self.__with_coref = bool(value)

    @property
    def with_constituents(self):
        return self.__with_constituents

    @with_constituents.setter
    def with_constituents(self, value):
        self.__with_constituents = bool(value)

    @property
    def with_expressions(self):
        return self.__with_expressions

    @with_expressions.setter
    def with_expressions(self, value):
        self.__with_expressions = bool(value)

    @property
    def with_dependencies(self):
        return self.__with_deps

    @with_dependencies.setter
    def with_dependencies(self, value):
        self.__with_deps = bool(value)

    @property
    def with_conll(self):
        return self.__with_process_conll

    @with_conll.setter
    def with_conll(self, value):
        self.__with_process_conll = bool(value)

    def check_output_format(self, output_format: str) -> str:
        """Clean up output format, check if it is valid before returning the normalized string"""
        f = output_format.lower().replace('-', '')
        if f not in self.allowed_formats:
            raise IOError(f'Allowed formats are {", ".join(self.allowed_formats)}')
        return f

    @staticmethod
    def normalize_language(language: str) -> str:
        """Returns a 2-letter language code"""
        return iso639.to_name(language).lower()

    def scrape_website(self, url: str) -> str:
        """Scrape the provided website, and return the text of its body"""
        # make sure the url is valid
        if 'http' != url[0:4]:
            url = f"http://{url}"
        # add a user-agent so we look like a browser
        response = requests.get(url, headers=({'User-Agent': self.user_agent}))
        if response.status_code > 201:
            raise IOError(f'Could not load {url}!')
        soup = BeautifulSoup(response.text, 'html.parser')
        # remove tags that should not be parsed for text
        for t in soup(['script', 'img', 'style', 'link']):
            t.extract()

        return '\n'.join(filter(lambda s: len(s) > 1, soup.find('body').text.split('\n')))

    def write_output(self, j: OrderedDict):
        if self.check_output_format(self.get_output_format()) == 'jsonnlp':
            return self.write_json(j)
        else:
            return self.write_text(to_conllu(j))

    def get_text(self) -> str:
        raise NotImplementedError

    def write_json(self, j: OrderedDict):
        raise NotImplementedError

    def write_text(self, conll: str):
        raise NotImplementedError

    def get_output_format(self) -> str:
        raise NotImplementedError

    def get_args(self) -> dict:
        raise NotImplementedError

    def handle_error(self, error: Exception):
        raise NotImplementedError

    def make_pipeline_args(self, style=Process.FULL) -> dict:
        # start with base params
        args = self.get_args()
        params = dict(args)
        # add process-specific params
        if style == Process.FULL:
            params['dependencies'] = True
            params['constituents'] = True
            params['coreferences'] = True
            params['expressions'] = True
        else:
            params['dependencies'] = style == Process.DEPS
            params['constituents'] = style == Process.CONST
            params['coreferences'] = style == Process.COREF
            params['expressions'] = style == Process.EXPR
        # allow for overrides of defaults
        params.update(args)
        # add text
        params['text'] = self.get_text()

        print(args)
        print(params)

        return params

    def run_pipeline(self, style: Process) -> OrderedDict:
        params = self.make_pipeline_args(style)
        return self.pipeline.process(**params)

    def process(self):
        try:
            return self.write_output(self.run_pipeline(Process.FULL))
        except Exception as e:
            return self.handle_error(e)

    def dependencies(self):
        try:
            if not self.with_dependencies:
                raise BrokenPipeError('This pipeline does not have a dependency parser')
            return self.write_output(self.run_pipeline(Process.DEPS))
        except Exception as e:
            return self.handle_error(e)

    def constituents(self):
        try:
            if not self.with_constituents:
                raise BrokenPipeError('This pipeline does not have a constituency parser')
            return self.write_output(self.run_pipeline(Process.CONST))
        except Exception as e:
            return self.handle_error(e)

    def token_list(self):
        try:
            return self.write_output(self.run_pipeline(Process.TOKENS))
        except Exception as e:
            return self.handle_error(e)

    def coreferences(self):
        try:
            if not self.with_coreferences:
                raise BrokenPipeError('This pipeline does not have a coreference parser')
            return self.write_output(self.run_pipeline(Process.COREF))
        except Exception as e:
            return self.handle_error(e)

    def expressions(self):
        try:
            if not self.with_expressions:
                raise BrokenPipeError('This pipeline does not have an expressions parser')
            return self.write_output(self.run_pipeline(Process.EXPR))
        except Exception as e:
            return self.handle_error(e)

    def custom_process(self, f):
        try:
            params = self.make_pipeline_args()
            return self.write_output(f(**params))
        except Exception as e:
            return self.handle_error(e)
