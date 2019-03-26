from collections import OrderedDict


class Pipeline(object):
    def process(self, text='') -> OrderedDict:
        raise NotImplementedError
