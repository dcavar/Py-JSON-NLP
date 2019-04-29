from collections import OrderedDict

from pyjsonnlp.annotation import Annotator
from pyjsonnlp.dependencies import UniversalDependencyParse


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
                        doc['relations'][r_id] = self.build_relation(r_id=r_id,
                                                                     predicate=sent['mainVerb'],
                                                                     p_from=sent['subject'],
                                                                     p_to=sent['object'])
                    elif sent.get('transitivity') == 'intransitive':
                        # these are attributes rather than relations (He died -> He is dead)
                        pass
                    elif sent.get('transitivity') == 'ditransitive':
                        pass
                        # the idea here is to combine the obj and iobj, but it needs more thought.
                        # trans_rel = self.build_relation(r_id=r_id, predicate=sent['mainVerb'],
                        #                                 p_from=sent['subject'],
                        #                                 p_to=sent['object'])
                        # intrans_rel = dict(trans_rel)
                        # doc['relations'][r_id] = trans_rel,
                        # r_id += 1
                        # intrans_rel['id'] = r_id,
                        # intrans_rel['predicate'].extend(intrans_rel['to'])
                        # intrans_rel['to'] = [t['id'] for t in d.get_leaves(sent['indirectObject'][0])]
                        # doc['relations'][r_id] = intrans_rel

                    r_id += 1

    @staticmethod
    def build_relation(r_id: int, predicate: dict, p_from: dict, p_to: dict) -> dict:
        return {
            'id': r_id,
            'predicate': predicate,
            'from': p_from,
            'to': p_to,
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
