from collections import OrderedDict, namedtuple
from typing import List, Union, Tuple, Dict

from pyjsonnlp.annotation import Annotator
from pyjsonnlp.tokenization import subtract_tokens

Dependency = namedtuple('Dep', 'dependent arc')  # int, str


class DependencyParse:
    def is_arc_present_below(self, token_id: int, arc: str) -> bool:
        raise NotImplementedError

    @property
    def style(self) -> str:
        raise NotImplementedError

    def get_leaves(self, token_id: int) -> List[OrderedDict]:
        raise NotImplementedError

    def get_leaves_by_arc(self, arc: str, head=None, sentence_id=1) -> Tuple[int, List[OrderedDict]]:
        raise NotImplementedError

    def get_child_with_arc(self, token_id: int, arc: str) -> Union[None, OrderedDict]:
        raise NotImplementedError

    def collect_compounds(self, token_id: int) -> List[OrderedDict]:
        raise NotImplementedError


class UniversalDependencyParse(DependencyParse):
    def __init__(self, dependencies: dict, tokens: OrderedDict):
        self.deps: dict = dependencies
        self.tokens: OrderedDict = tokens
        self.nodes: Dict[int, List[Dependency]] = {}
        self.sentence_heads: Dict[int, int] = {}  # sentenceId -> head
        if dependencies.get('style', 'universal') != 'universal':
            raise ValueError(f"{dependencies['style']} is not universal!")
        self._build_nodes()

    def _build_nodes(self):
        for t in self.tokens.values():
            arc: dict = self.deps['arcs'][t['id']][0]
            if arc['governor'] not in self.nodes:
                self.nodes[arc['governor']] = []
            if arc['governor'] == 0:
                self.sentence_heads[arc['sentenceId']] = t['id']
            self.nodes[arc['governor']].append(Dependency(dependent=arc['dependent'], arc=arc['label']))

    def is_arc_present_below(self, token_id: int, arc: str) -> bool:
        stack = list(self.nodes.get(token_id, []))
        while len(stack):
            dep = stack.pop()
            if dep.arc == arc:
                return True
            stack.extend(self.nodes.get(dep.dependent, []))
        return False

    @property
    def style(self) -> str:
        return self.deps.get('style', 'universal')

    def get_leaves(self, token_id: int) -> List[OrderedDict]:
        tokens = [self.tokens[token_id]]
        stack = list(self.nodes.get(token_id, []))
        while len(stack):
            dep = stack.pop()
            tokens.append(self.tokens[dep.dependent])
            stack.extend(self.nodes.get(dep.dependent, []))

        return sorted(tokens, key=lambda t: t['id'])

    def get_leaves_by_arc(self, arc: str, head=None, sentence_id=1) -> Tuple[int, List[OrderedDict]]:
        if head is None:
            head = self.sentence_heads[sentence_id]
        stack = list(self.nodes.get(head, []))
        while len(stack):
            dep = stack.pop()
            if dep.arc == arc:
                return dep.dependent, self.get_leaves(dep.dependent)
            stack.extend(self.nodes.get(dep.dependent, []))
        return 0, []

    def get_child_with_arc(self, token_id: int, arc: str, follow: Tuple = ()) -> Union[None, OrderedDict]:
        stack = list(self.nodes.get(token_id, []))
        while len(stack):
            dep = stack.pop()
            if dep.arc == arc:
                return self.tokens[dep.dependent]
            if dep.arc in follow:
                stack.extend(self.nodes.get(dep.dependent, []))
        return None

    def collect_compounds(self, token_id: int) -> List[OrderedDict]:
        compound = [self.tokens[token_id]]
        stack = list(self.nodes.get(token_id, []))
        while len(stack):
            dep = stack.pop()
            if dep.arc == 'compound':
                compound.append(self.tokens[dep.dependent])
                stack.extend(self.nodes.get(dep.dependent, []))

        return sorted(compound, key=lambda t: t['id'])


class DependencyAnnotator(Annotator):
    clause_arcs = ('csubj', 'ccomp', 'xcomp', 'advcl', 'acl')
    clause_types = (('csubj', 'subject'), ('xcomp', 'relative'), ('ccomp', 'complement'), ('advcl', 'adverbial'), ('acl', 'adjectival'))
    compound_arcs = ('conj', 'cc')
    sov = (('subject', 'nsubj', ()),
           ('object', 'obj', ()),
           ('object', 'dobj', ()),
           ('indirectObject', 'iobj', ()),
           ('indirectObject', 'dative', ()))

    def annotate(self, nlp_json: OrderedDict) -> None:
        for doc in nlp_json['documents'].values():
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
                parent_clause_id = 0
                item_tokens = [d.tokens[t_id] for t_id in range(sent['tokenFrom'], sent['tokenTo'])]
                while item['complex']:
                    if 'clauses' not in doc:
                        doc['clauses'] = {}
                    for arc, clause_type in self.clause_types:
                        if d.is_arc_present_below(item_head, arc):
                            # clause
                            c_head, clause_tokens = d.get_leaves_by_arc(arc, head=item_head, sentence_id=s_id)
                            clause = self.build_clause(c_id, s_id, parent_clause_id, clause_type, clause_tokens)
                            doc['clauses'][c_id] = clause
                            self.annotate_item(d, c_head, clause)
                            parent_clause_id = c_id
                            c_id += 1

                            # matrix clause at the sentence level
                            if depth == 0:
                                matrix_tokens = subtract_tokens(item_tokens, clause_tokens)
                                matrix = self.build_clause(c_id, s_id, 0, 'matrix', matrix_tokens)
                                doc['clauses'][c_id] = matrix
                                clause['parentClauseId'] = c_id
                                self.annotate_item(d, s_head, matrix)
                                c_id += 1

                            depth += 1
                            item = clause
                            item_head = c_head
                            # don't need item tokens
                            break

    @staticmethod
    def build_clause(clause_id: int, sent_id: int, parent_clause_id: int, clause_type: str, tokens: List[dict]) -> dict:
        clause = {
            'id': clause_id,
            'sentenceId': sent_id,
            'clauseType': clause_type,
            'tokens': [t['id'] for t in tokens]
        }
        if parent_clause_id:
            clause['parentClauseId'] = parent_clause_id
        return clause

    @staticmethod
    def build_grammar(d: UniversalDependencyParse, head: int) -> dict:
        return {
            'head': head,
            'semantic': [t['id'] for t in d.collect_compounds(head)],
            'phrase': [t['id'] for t in d.get_leaves(head)]
        }

    def annotate_item(self, d: UniversalDependencyParse, head: int, item: dict) -> None:
        # root
        item['root'] = [head]

        # subject/object/verb
        if d.tokens[head]['upos'][0] == 'V' or d.tokens[head]['xpos'][0] == 'V':
            item['mainVerb'] = self.build_grammar(d, head)
        for k, arc, follow in self.sov:
            grammar_head = d.get_child_with_arc(head, arc, follow)
            if grammar_head:
                item[k] = self.build_grammar(d, grammar_head['id'])

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
            elif not item['complex'] and d.is_arc_present_below(head, 'nsubj'):
                item['transitivity'] = 'intransitive'

        # negation
        item['negated'] = bool(d.get_child_with_arc(head, 'neg'))

        # todo sentence types
        # todo tense
        # todo modality
