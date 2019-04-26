from collections import OrderedDict
from typing import Dict, List

from pyjsonnlp.annotation import Annotator
from pyjsonnlp.dependencies import UniversalDependencyParse, DependencyParse


class RelationAnnotator(Annotator):
    def annotate(self, nlp_json: OrderedDict) -> None:
        for doc in nlp_json['documents'].values():
            if 'relations' not in doc:
                doc['relations'] = {}
            r_id = len(doc['relations']) + 1
            d = UniversalDependencyParse(doc['dependencies'][0], doc['tokenList'])
            for s_id, sent in doc['sentences'].items():
                if 'complex' not in sent:
                    raise BrokenPipeError('You must do clause extraction first!')
                if not sent['complex']:
                    if sent.get('transitivity') == 'transitive':
                        doc['relations'][r_id] = self.build_relation(d, r_id=r_id,
                                                                     predicate_head=sent['mainVerb'][0],
                                                                     from_head=sent['subject'][0],
                                                                     to_head=sent['object'][0])
                    elif sent.get('transitivity') == 'intransitive':
                        # these are attributes rather than relations (He died -> He is dead)
                        pass
                    elif sent.get('transitivity') == 'ditransitive':
                        trans_rel = self.build_relation(d, r_id=r_id, predicate_head=sent['mainVerb'][0],
                                                        from_head=sent['subject'][0],
                                                        to_head=sent['object'][0])
                        intrans_rel = dict(trans_rel)
                        doc['relations'][r_id] = trans_rel,
                        r_id += 1
                        intrans_rel['id'] = r_id,
                        intrans_rel['predicate'].extend(intrans_rel['to'])
                        intrans_rel['to'] = [t['id'] for t in d.get_leaves(sent['indirectObject'][0])]
                        doc['relations'][r_id] = intrans_rel

                    r_id += 1

    @staticmethod
    def build_relation(d: DependencyParse, r_id: int, predicate_head: int, from_head: int, to_head: int) -> Dict[str, List[int]]:
        return {
            'id': r_id,
            'predicate': [t['id'] for t in d.get_leaves(predicate_head)],
            'from': [t['id'] for t in d.get_leaves(from_head)],
            'to': [t['id'] for t in d.get_leaves(to_head)],
        }


class PresuppositionRelationAnnotator(Annotator):
    def annotate(self, nlp_json: OrderedDict) -> None:
        for doc in nlp_json['documents'].values():
            if 'relations' not in doc:
                doc['relations'] = {}
            r_id = len(doc['relations']) + 1
            d = UniversalDependencyParse(doc['dependencies'][0], doc['tokenList'])
            for s_id, sent in doc['sentences'].items():
                pass


def write_snap(nlp_json: OrderedDict, file='relations.csv'):
    for doc in nlp_json.get('documents', {}).values():
        for rel in doc.get('relations', {}).values():
            pass
