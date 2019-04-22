from collections import OrderedDict
from unittest import TestCase

import pytest

from pyjsonnlp.unification import Unifier, UnificationError


def build_json() -> OrderedDict:
    return OrderedDict({
        'documents': {
            1: {
                'tokenList': {
                    1: {'id': 1, 'text': 'a'},
                    2: {'id': 2, 'text': 'b'},
                    3: {'id': 3, 'text': 'c'},
                    4: {'id': 4, 'text': 'd'},
                },
                'clauses': {
                    1: {'sentenceId': 1, 'id': 1, 'tokens': [1, 2], 'root': 1},
                    2: {'sentenceId': 1, 'id': 2, 'tokens': [3, 4], 'root': 3}
                },
                'sentences': {
                    1: {'id': 1, 'tokenFrom': 1, 'tokenTo': 5, 'clauses': [1, 2], 'object': [1]}
                },
                'paragraphs': {
                    1: {'id': 1, 'tokens': [1, 2, 3, 4]}
                },
                'dependencies': [{
                    'arcs': {
                        1: [{'governor': 2}],
                        2: [{'governor': 3}]
                    }
                }],
                'coreferences': [
                    {
                        'id': 1,
                        'representative': {
                            'head': 1,
                            'tokens': [1, 2]
                        },
                        'referents': [{
                            'head': 3,
                            'tokens': [3, 4]
                        }]
                    },
                    {
                        'id': 2,
                        'representative': {
                            'head': 2,
                            'tokens': [1, 2]
                        },
                        'referents': [{
                            'head': 3,
                            'tokens': [3, 4]
                        }]
                    }
                ],
                'constituents': [{
                    'sentenceId': 1
                }],
                'expressions': [{
                    'id': 1,
                    'head': 1,
                    'tokens': [1]
                }]
            }
        }})


class TestUnification(TestCase):
    def setUp(self) -> None:
        self.u = Unifier()

    def test_overwrite_annotation_from_a_with_b_tokens(self):
        a = build_json()
        b = build_json()
        a['documents'][1]['tokenList'][1]['orig'] = 1
        a['documents'][1]['tokenList'][1]['both'] = 1
        b['documents'][1]['tokenList'][1]['both'] = 2
        b['documents'][1]['tokenList'][1]['new'] = 1
        b['documents'][1]['tokenList'][1]['new_dict'] = {'a': 1}
        a['documents'][1]['tokenList'][1]['dict'] = {'a': 1}
        b['documents'][1]['tokenList'][1]['dict'] = {'a': 1}
        b['documents'][1]['tokenList'][1]['dict']['b'] = 2
        a['documents'][1]['tokenList'][1]['dict']['c'] = 3
        actual = self.u.overwrite_annotation_from_a_with_b(a, b, 'tokens')
        expected = OrderedDict([('documents', {1: OrderedDict([('tokenList', {1: {'id': 1, 'text': 'a', 'orig': 1, 'both': 2, 'dict': {'a': 1, 'c': 3, 'b': 2}, 'new': 1, 'new_dict': {'a': 1}}, 2: {'id': 2, 'text': 'b'}, 3: {'id': 3, 'text': 'c'}, 4: {'id': 4, 'text': 'd'}}), ('clauses', {1: {'sentenceId': 1, 'id': 1, 'tokens': [1, 2], 'root': 1}, 2: {'sentenceId': 1, 'id': 2, 'tokens': [3, 4], 'root': 3}}), ('sentences', {1: {'id': 1, 'tokenFrom': 1, 'tokenTo': 5, 'clauses': [1, 2], 'object': [1]}}), ('paragraphs', {1: {'id': 1, 'tokens': [1, 2, 3, 4]}}), ('dependencies', [{'arcs': {1: [{'governor': 2}], 2: [{'governor': 3}]}}]), ('coreferences', [{'id': 1, 'representative': {'head': 1, 'tokens': [1, 2]}, 'referents': [{'head': 3, 'tokens': [3, 4]}]}, {'id': 2, 'representative': {'head': 2, 'tokens': [1, 2]}, 'referents': [{'head': 3, 'tokens': [3, 4]}]}]), ('constituents', [{'sentenceId': 1}]), ('expressions', [{'id': 1, 'head': 1, 'tokens': [1]}])])})])
        assert expected == actual, actual

    def test_merge_tokens(self):
        a = [1, 2, 3]
        b = [2, 3, 4]
        actual = self.u.merge_tokens(a, b)
        expected = [1, 2, 3, 4]
        assert expected == actual, actual

    def test_add_annotation_to_a_from_b_errors(self):
        a = build_json()
        b = build_json()
        with pytest.raises(UnificationError):
            self.u.add_annotation_to_a_from_b(a, b, 'nonsense')
        with pytest.raises(UnificationError):
            del a['documents'][1]['tokenList'][2]
            self.u.add_annotation_to_a_from_b(a, b, 'tokens')

    def test_add_annotation_to_a_from_b_expressions(self):
        a = build_json()
        b = build_json()
        b['documents'][1]['expressions'].append({'id': 2})
        actual = self.u.add_annotation_to_a_from_b(a, b, 'expressions')
        expected = OrderedDict([('documents', {1: OrderedDict([('tokenList', {1: {'id': 1, 'text': 'a'}, 2: {'id': 2, 'text': 'b'}, 3: {'id': 3, 'text': 'c'}, 4: {'id': 4, 'text': 'd'}}), ('clauses', {1: {'sentenceId': 1, 'id': 1, 'tokens': [1, 2], 'root': 1}, 2: {'sentenceId': 1, 'id': 2, 'tokens': [3, 4], 'root': 3}}), ('sentences', {1: {'id': 1, 'tokenFrom': 1, 'tokenTo': 5, 'clauses': [1, 2], 'object': [1]}}), ('paragraphs', {1: {'id': 1, 'tokens': [1, 2, 3, 4]}}), ('dependencies', [{'arcs': {1: [{'governor': 2}], 2: [{'governor': 3}]}}]), ('coreferences', [{'id': 1, 'representative': {'head': 1, 'tokens': [1, 2]}, 'referents': [{'head': 3, 'tokens': [3, 4]}]}, {'id': 2, 'representative': {'head': 2, 'tokens': [1, 2]}, 'referents': [{'head': 3, 'tokens': [3, 4]}]}]), ('constituents', [{'sentenceId': 1}]), ('expressions', [{'id': 1, 'head': 1, 'tokens': [1]}, {'id': 2, 'head': 1, 'tokens': [1]}, {'id': 4}])])})])
        assert expected == actual, actual

    def test_add_annotation_to_a_from_b_coreferences_new_same_head(self):
        a = build_json()
        b = build_json()
        b['documents'][1]['coreferences'].append({
                        'id': 3,
                        'representative': {
                            'head': 1,
                            'tokens': [1, 2]
                        },
                        'referents': [{
                            'head': 3,
                            'tokens': [3, 4]
                        }]})
        actual = self.u.add_annotation_to_a_from_b(a, b, 'coreferences')
        assert len(actual['documents'][1]['coreferences']) == 2, len(actual['documents'][1]['coreferences'])
    
    def test_add_annotation_to_a_from_b_coreferences_new(self):
        a = build_json()
        b = build_json()
        b['documents'][1]['coreferences'].append({
                        'id': 3,
                        'representative': {
                            'head': 3,
                            'tokens': [1, 2]
                        },
                        'referents': [{
                            'head': 3,
                            'tokens': [3, 4]
                        }]})
        actual = self.u.add_annotation_to_a_from_b(a, b, 'coreferences')
        assert len(actual['documents'][1]['coreferences']) == 3, len(actual['documents'][1]['coreferences'])

    def test_add_annotation_to_a_from_b_coreferences_new_properties(self):
        a = build_json()
        b = build_json()
        b['documents'][1]['coreferences'][0]['representative']['type'] = 'test'
        actual = self.u.add_annotation_to_a_from_b(a, b, 'coreferences')
        assert actual['documents'][1]['coreferences'][0]['representative']['type'] == 'test'

    def test_add_annotation_to_a_from_b_tokens(self):
        a = build_json()
        b = build_json()
        b['documents'][1]['tokenList'][1]['new'] = 1
        b['documents'][1]['tokenList'][1]['new_dict'] = {'a': 1}
        a['documents'][1]['tokenList'][1]['dict'] = {'a': 1}
        b['documents'][1]['tokenList'][1]['dict'] = {'a': 1}
        b['documents'][1]['tokenList'][1]['dict']['b'] = 2
        a['documents'][1]['tokenList'][1]['dict']['c'] = 3
        actual = self.u.add_annotation_to_a_from_b(a, b, 'tokens')
        expected = OrderedDict([('documents', {1: OrderedDict([('tokenList', {1: {'id': 1, 'text': 'a', 'dict': {'a': 1, 'c': 3, 'b': 2}, 'new': 1, 'new_dict': {'a': 1}}, 2: {'id': 2, 'text': 'b'}, 3: {'id': 3, 'text': 'c'}, 4: {'id': 4, 'text': 'd'}}), ('clauses', {1: {'sentenceId': 1, 'id': 1, 'tokens': [1, 2], 'root': 1}, 2: {'sentenceId': 1, 'id': 2, 'tokens': [3, 4], 'root': 3}}), ('sentences', {1: {'id': 1, 'tokenFrom': 1, 'tokenTo': 5, 'clauses': [1, 2], 'object': [1]}}), ('paragraphs', {1: {'id': 1, 'tokens': [1, 2, 3, 4]}}), ('dependencies', [{'arcs': {1: [{'governor': 2}], 2: [{'governor': 3}]}}]), ('coreferences', [{'id': 1, 'representative': {'head': 1, 'tokens': [1, 2]}, 'referents': [{'head': 3, 'tokens': [3, 4]}]}, {'id': 2, 'representative': {'head': 2, 'tokens': [1, 2]}, 'referents': [{'head': 3, 'tokens': [3, 4]}]}]), ('constituents', [{'sentenceId': 1}]), ('expressions', [{'id': 1, 'head': 1, 'tokens': [1]}])])})])
        assert expected == actual, actual

    def test_extend_a_with_b(self):
        a = build_json()
        b = build_json()
        actual = self.u.extend_a_with_b(a, b)
        expected = OrderedDict([('documents', {1: OrderedDict([('tokenList', {1: {'id': 1, 'text': 'a'}, 2: {'id': 2, 'text': 'b'}, 3: {'id': 3, 'text': 'c'}, 4: {'id': 4, 'text': 'd'}, 5: {'id': 5, 'text': 'a'}, 6: {'id': 6, 'text': 'b'}, 7: {'id': 7, 'text': 'c'}, 8: {'id': 8, 'text': 'd'}}), ('clauses', {1: {'sentenceId': 1, 'id': 1, 'tokens': [1, 2], 'root': 1}, 2: {'sentenceId': 1, 'id': 2, 'tokens': [3, 4], 'root': 3}, 3: {'sentenceId': 2, 'id': 3, 'tokens': [5, 6], 'root': 5}, 4: {'sentenceId': 2, 'id': 4, 'tokens': [7, 8], 'root': 7}}), ('sentences', {1: {'id': 1, 'tokenFrom': 1, 'tokenTo': 5, 'clauses': [1, 2], 'object': [1]}, 2: {'id': 2, 'tokenFrom': 5, 'tokenTo': 9, 'clauses': [3, 4], 'object': [5]}}), ('paragraphs', {1: {'id': 1, 'tokens': [1, 2, 3, 4]}, 2: {'id': 2, 'tokens': [5, 6, 7, 8]}}), ('dependencies', [{'arcs': {1: [{'governor': 2}], 2: [{'governor': 3}]}}, {'arcs': {9: [{'governor': 10}], 10: [{'governor': 11}]}}]), ('coreferences', [{'id': 1, 'representative': {'head': 1, 'tokens': [1, 2]}, 'referents': [{'head': 3, 'tokens': [3, 4]}]}, {'id': 2, 'representative': {'head': 2, 'tokens': [1, 2]}, 'referents': [{'head': 3, 'tokens': [3, 4]}]}, {'id': 3, 'representative': {'head': 5, 'tokens': [5, 6]}, 'referents': [{'head': 7, 'tokens': [7, 8]}]}, {'id': 4, 'representative': {'head': 6, 'tokens': [5, 6]}, 'referents': [{'head': 7, 'tokens': [7, 8]}]}]), ('constituents', [{'sentenceId': 1}, {'sentenceId': 2}]), ('expressions', {'id': 2, 'head': 5, 'tokens': [5]})])})])
        assert expected == actual, actual

    def test_extend_a_with_b_no_side_effects(self):
        a = build_json()
        b = build_json()
        a_copy = OrderedDict(a)
        b_copy = OrderedDict(b)
        self.u.extend_a_with_b(a, b)
        assert a_copy == a, a
        assert b_copy == b, b
