from collections import OrderedDict, namedtuple
from typing import List, Union, Tuple, Dict

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
    def __init__(self, dependencies: dict, tokens: list):
        self.deps: dict = dependencies
        self.tokens: list = tokens
        self.nodes: Dict[int, List[Dependency]] = {}
        self.sentence_heads: Dict[int, int] = {}  # sentenceId -> head
        if dependencies.get('style', 'universal') != 'universal':
            raise ValueError(f"{dependencies['style']} is not universal!")
        self._build_nodes()

    def _build_nodes(self):
        for t in self.tokens:
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
        tokens = [self.tokens[token_id-1]]
        stack = list(self.nodes.get(token_id, []))
        while len(stack):
            dep = stack.pop()
            tokens.append(self.tokens[dep.dependent-1])
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
                return self.tokens[dep.dependent-1]
            if dep.arc in follow:
                stack.extend(self.nodes.get(dep.dependent, []))
        return None

    def collect_compounds(self, token_id: int) -> List[OrderedDict]:
        compound = [self.tokens[token_id-1]]
        stack = list(self.nodes.get(token_id, []))
        while len(stack):
            dep = stack.pop()
            if dep.arc == 'compound':
                compound.append(self.tokens[dep.dependent-1])
                stack.extend(self.nodes.get(dep.dependent, []))

        return sorted(compound, key=lambda t: t['id'])
