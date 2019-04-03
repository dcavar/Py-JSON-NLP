#!/usr/bin/env python3

"""
(C) 2019 Damir Cavar, Oren Baldinger, Maanvitha Gongalla, Anurag Kumar, Murali Kammili


Interface for the NLP pipelines.


Licensed under the Apache License 2.0, see the file LICENSE for more details.


Brought to you by the NLP-Lab.org (https://nlp-lab.org/)!
"""

from collections import OrderedDict


class Pipeline(object):
    @staticmethod
    def process(text='', coreferences=False, constituents=False, dependencies=False, expressions=False, **kwargs) -> OrderedDict:
        raise NotImplementedError
