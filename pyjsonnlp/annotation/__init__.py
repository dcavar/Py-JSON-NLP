from collections import OrderedDict


class Annotator:
    def annotate(self, nlp_json: OrderedDict) -> None:
        raise NotImplementedError