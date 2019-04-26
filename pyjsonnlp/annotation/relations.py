from collections import OrderedDict

from pyjsonnlp.annotation import Annotator
from pyjsonnlp.dependencies import UniversalDependencyParse, DependencyParse


class RelationAnnotator(Annotator):
    def __init__(self):
        self.d: DependencyParse

    def annotate(self, nlp_json: OrderedDict) -> None:
        for doc in nlp_json['documents'].values():
            r_id = 1
            self.d = UniversalDependencyParse(doc['dependencies'][0], doc['tokenList'])
            for s_id, sent in doc['sentences'].items():
                if 'complex' not in sent:
                    raise BrokenPipeError('You must do clause extraction first!')
                if not sent['complex']:
                    if sent['transitivity'] == 'transitive':
                        if 'relations' not in doc:
                            doc['relations'] = {}
                        doc['relations'][r_id] = self.build_relation(r_id=r_id,
                                                                     predicate_head=sent['mainVerb'][0],
                                                                     from_head=sent['subject'][0],
                                                                     to_head=sent['object'][0])
                        r_id += 1

    def build_relation(self, r_id: int, predicate_head: int, from_head: int, to_head: int) -> dict:
        return {
            'id': r_id,
            'predicate': [t['id'] for t in self.d.get_leaves(predicate_head)],
            'from': [t['id'] for t in self.d.get_leaves(from_head)],
            'to': [t['id'] for t in self.d.get_leaves(to_head)],
        }
