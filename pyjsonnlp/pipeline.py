#!/usr/bin/env python3

"""
(C) 2019 Damir Cavar, Oren Baldinger, Maanvitha Gongalla, Anurag Kumar, Murali Kammili


Dependable interface for the NLP pipelines.


Licensed under the Apache License 2.0, see the file LICENSE for more details.


Brought to you by the NLP-Lab.org (https://nlp-lab.org/)!
"""


from collections import OrderedDict


class Pipeline(object):
    def process(self, text='') -> OrderedDict:
        raise NotImplementedError
