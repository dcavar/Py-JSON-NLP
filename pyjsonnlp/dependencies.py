from collections import OrderedDict
from typing import List, Union, Tuple

from pyjsonnlp.tokenization import subtract_tokens


class UniversalDependencyParse:
    def __init__(self, dependencies: dict, tokens: OrderedDict):
        self.deps = dependencies
        self.tokens = tokens
        self.nodes = {}
        self.sentence_heads = {}  # sentenceId -> head
        if dependencies.get('style', 'universal') != 'universal':
            raise ValueError(f"{dependencies['style']} is not universal!")
        self._build_nodes()

    def _build_nodes(self):
        for t in self.tokens.values():
            arc = self.deps['arcs'][t['id']][0]
            if arc['governor'] not in self.nodes:
                self.nodes[arc['governor']] = []
            if arc['governor'] == 0:
                self.sentence_heads[arc['sentenceId']] = t['id']
            self.nodes[arc['governor']].append((arc['dependent'], arc['label']))

    def is_arc_present_below(self, token_id: int, arc: str) -> bool:
        stack = list(self.nodes.get(token_id, []))
        while len(stack):
            dep = stack.pop()
            if dep[1] == arc:
                return True
            stack.extend(self.nodes.get(dep[0], []))
        return False

    @property
    def style(self) -> str:
        return self.deps.get('style', 'universal')

    def get_leaves(self, token_id: int) -> List[OrderedDict]:
        tokens = [self.tokens[token_id]]
        stack = list(self.nodes.get(token_id, []))
        while len(stack):
            dep = stack.pop()
            tokens.append(self.tokens[dep[0]])
            stack.extend(self.nodes.get(dep[0], []))

        return sorted(tokens, key=lambda t: t['id'])

    def get_leaves_by_arc(self, arc: str, sentence_id=1) -> Tuple[int, List[OrderedDict]]:
        stack = list(self.nodes.get(self.sentence_heads[sentence_id], []))
        while len(stack):
            dep = stack.pop()
            if dep[1] == arc:
                return dep[0], self.get_leaves(dep[0])
            stack.extend(self.nodes.get(dep[0], []))
        return 0, []

    def get_child_with_arc(self, token_id: int, arc: str) -> Union[None, OrderedDict]:
        for dep, label in self.nodes.get(token_id, []):
            if label == arc:
                return dep
        return None


class Annotator:
    def annotate(self, nlp_json: OrderedDict) -> None:
        pass


class DependencyAnnotator(Annotator):
    clause_arcs = ('csubj', 'ccomp', 'xcomp', 'advcl', 'acl')
    clause_types = (('csubj', 'subject'), ('xcomp', 'relative'), ('ccomp', 'complement'), ('advcl', 'adverbial'), ('acl', 'adjectival'))
    compound_arcs = ('conj', 'cc')

    def annotate(self, nlp_json: OrderedDict) -> None:
        for doc in nlp_json['documents']:
            c_id = 1
            d = UniversalDependencyParse(doc['dependencies'][0], doc['tokenList'])
            for s_id, sent in doc['sentences'].items():
                s_head = d.sentence_heads[s_id]

                # subject/object/verb
                self.annotate_item(d, s_head, sent)

                # clauses
                depth = 0
                item = sent
                item_head = s_head
                item_tokens = [d.tokens[t_id] for t_id in range(sent['tokenFrom'], sent['tokenTo'])]
                while item['complex']:
                    if 'clauses' not in doc:
                        doc['clauses'] = {}
                    for arc, clause_type in self.clause_types:
                        if d.is_arc_present_below(item_head, arc):
                            # clause
                            c_head, clause_tokens = d.get_leaves_by_arc(arc, item_head)
                            clause = self.build_clause(c_id, s_id, clause_type, clause_tokens)
                            doc['clauses'][c_id] = clause
                            self.annotate_item(d, c_head, clause)
                            c_id += 1

                            # matrix clause at the sentence level
                            if depth == 0:
                                matrix_tokens = subtract_tokens(item_tokens, clause_tokens)
                                matrix = self.build_clause(c_id, s_id, 'matrix', matrix_tokens)
                                doc['clauses'][c_id] = matrix
                                self.annotate_item(d, s_head, matrix)

                            depth += 1
                            item = clause
                            item_head = c_head
                            # don't need item tokens
                            break

    @staticmethod
    def build_clause(clause_id: int, sent_id: int, clause_type: str, tokens: List[dict]) -> dict:
        return {
            'id': clause_id,
            'sentenceId': sent_id,
            'clause_type': clause_type,
            'tokens': [t['id'] for t in tokens]
        }

    def annotate_item(self, d: UniversalDependencyParse, head: int, item: dict) -> None:
        # root
        item['root'] = [head]

        # subject/object/verb
        if d.tokens[head]['upos'] == 'VERB':
            item['mainVerb'] = [head]
        for k, arc in (('subject', 'nsubj'), ('object', 'obj'), ('indirectObject', 'iobj'), ('indirectObject', 'dative')):
            v = d.get_child_with_arc(head, arc)
            if v:
                item[k] = v

        # compound/complex/fragment
        item['compound'] = any(map(lambda a: d.is_arc_present_below(head, a), self.compound_arcs))
        item['complex'] = any(map(lambda a: d.is_arc_present_below(head, a), self.clause_arcs))
        # todo fragment (the syntax parser will tell this)

        # transitivity
        if 'mainVerb' in item:
            if 'indirectObject' in item:
                item['transitivity'] = 'ditransitive'
            elif 'object' in item:
                item['transitivity'] = 'transitive'
            elif not item['complex']:
                item['transitivity'] = 'intransitive'

        # negation
        item['negated'] = bool(d.get_child_with_arc(head, 'neg'))

        # todo sentence types
        # todo modality


class Relations:
    def extract(self) -> None:
        pass
