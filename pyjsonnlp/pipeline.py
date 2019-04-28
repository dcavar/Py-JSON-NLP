"""
(C) 2019 Damir Cavar, Oren Baldinger, Maanvitha Gongalla, Anurag Kumar, Murali Kammili

Interface for the NLP pipelines.
Licensed under the Apache License 2.0, see the file LICENSE for more details.
Brought to you by the NLP-Lab.org (https://nlp-lab.org/)!
"""

from collections import OrderedDict
import requests


class Pipeline(object):
    """An interface for NLP-Json pipelines"""
    @staticmethod
    def process(text='', coreferences=False, constituents=False, dependencies=False, expressions=False, **kwargs) -> OrderedDict:
        raise NotImplementedError

    def process_conll(self, conll='', coreferences=False, constituents=False, dependencies=False, expressions=False,
                      **kwargs):
        pass


class RemotePipeline(Pipeline):
    """This class providers a local endpoint for a Pipeline deployed remotely as a microservice"""
    def __init__(self, url, port=False):
        super(RemotePipeline, self).__init__()
        self._url = url
        self._port = port

    @property
    def url(self):
        return ('http://' if self._url[0:4] != 'http' else '') + \
               (self._url if self._url[-1] != '/' else self._url[:-1]) + \
               (':' + str(self._port) if self._port else '')

    def process(self, text='', coreferences=False, constituents=False, dependencies=False, expressions=False,
                **kwargs) -> OrderedDict:
        params = {
            'text': text,
            'coreferences': coreferences,
            'constituents': constituents,
            'dependencies': dependencies,
            'expressions': expressions
        }
        params.update(kwargs)
        r = requests.post(self.url, data=params)
        if r.status_code != 200 and r.status_code != 201:
            raise BrokenPipeError(f'{r.reason} from {self.url} ({r.status_code})')

        return RemotePipeline.to_python(r.json())

    def process_conll(self, conll='', coreferences=False, constituents=False, dependencies=False, expressions=False,
                      **kwargs):
        if conll == '':
            raise ValueError('You must pass something in the conll parameter!')

        params = {
            'conll': conll,
            'coreferences': coreferences,
            'constituents': constituents,
            'dependencies': dependencies,
            'expressions': expressions
        }
        params.update(kwargs)

        url = self.url + '/process_conll'
        r = requests.post(url, data=params)
        if r.status_code != 200 and r.status_code != 201:
            raise BrokenPipeError(f'{r.reason} from {url} ({r.status_code})')

        return RemotePipeline.to_python(r.json())

    @staticmethod
    def to_python(json_data: dict) -> OrderedDict:
        """Convert sting dict keys to integer"""
        corrected = OrderedDict()

        for key, value in json_data.items():
            if isinstance(value, list):
                value = [RemotePipeline.to_python(item) if isinstance(item, dict) else item
                         for item in value]
            elif isinstance(value, dict):
                value = RemotePipeline.to_python(value)
            try:
                key = int(key)
            except Exception:
                pass
            corrected[key] = value

        return corrected
