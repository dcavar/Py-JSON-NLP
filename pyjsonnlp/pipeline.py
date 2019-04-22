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
            'coreferences': int(coreferences),
            'constituents': int(constituents),
            'dependencies': int(dependencies),
            'expressions': int(expressions)
        }
        params.update(kwargs)
        r = requests.post(self.url, data=params)
        if r.status_code != 200 and r.status_code != 201:
            raise BrokenPipeError(f'{r.reason} from {self.url} ({r.status_code})')

        return OrderedDict(r.json())
