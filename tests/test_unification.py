from collections import OrderedDict
from unittest import TestCase

import pytest

from pyjsonnlp.unification import Unifier, UnificationError


def build_json() -> OrderedDict:
    return OrderedDict({
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
                        'head': 1,
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
        })


class TestUnification(TestCase):
    def test_overwrite_annotation_from_a_with_b_tokens(self):
        unifier = Unifier()
        a = build_json()
        b = build_json()
        a['tokenList'][1]['orig'] = 1
        a['tokenList'][1]['both'] = 1
        b['tokenList'][1]['both'] = 2
        b['tokenList'][1]['new'] = 1
        b['tokenList'][1]['new_dict'] = {'a': 1}
        a['tokenList'][1]['dict'] = {'a': 1}
        b['tokenList'][1]['dict'] = {'a': 1}
        b['tokenList'][1]['dict']['b'] = 2
        a['tokenList'][1]['dict']['c'] = 3
        actual = unifier.overwrite_annotation_from_a_with_b(a, b, 'tokens')
        expected = OrderedDict([('tokenList', {1: {'id': 1, 'text': 'a', 'orig': 1, 'both': 2, 'dict': {'a': 1, 'c': 3, 'b': 2}, 'new': 1, 'new_dict': {'a': 1}}, 2: {'id': 2, 'text': 'b'}, 3: {'id': 3, 'text': 'c'}, 4: {'id': 4, 'text': 'd'}}), ('clauses', {1: {'sentenceId': 1, 'id': 1, 'tokens': [1, 2], 'root': 1}, 2: {'sentenceId': 1, 'id': 2, 'tokens': [3, 4], 'root': 3}}), ('sentences', {1: {'id': 1, 'tokenFrom': 1, 'tokenTo': 5, 'clauses': [1, 2], 'object': [1]}}), ('paragraphs', {1: {'id': 1, 'tokens': [1, 2, 3, 4]}}), ('dependencies', [{'arcs': {1: [{'governor': 2}], 2: [{'governor': 3}]}}]), ('coreferences', [{'id': 1, 'representative': {'head': 1, 'tokens': [1, 2]}, 'referents': [{'head': 3, 'tokens': [3, 4]}]}, {'id': 2, 'representative': {'head': 1, 'tokens': [1, 2]}, 'referents': [{'head': 3, 'tokens': [3, 4]}]}]), ('constituents', [{'sentenceId': 1}]), ('expressions', [{'id': 1, 'head': 1, 'tokens': [1]}])])
        assert expected == actual, actual

    def test_add_annotation_to_a_from_b_errors(self):
        unifier = Unifier()
        a = build_json()
        b = build_json()
        with pytest.raises(UnificationError):
            unifier.add_annotation_to_a_from_b(a, b, 'nonsense')
        with pytest.raises(UnificationError):
            del a['tokenList'][2]
            unifier.add_annotation_to_a_from_b(a, b, 'tokens')

    def test_add_annotation_to_a_from_b_expressions(self):
        unifier = Unifier()
        a = build_json()
        b = build_json()
        b['expressions'].append({'id': 2})
        actual = unifier.add_annotation_to_a_from_b(a, b, 'expressions')
        expected = OrderedDict([('tokenList', {1: {'id': 1, 'text': 'a'}, 2: {'id': 2, 'text': 'b'}, 3: {'id': 3, 'text': 'c'}, 4: {'id': 4, 'text': 'd'}}), ('clauses', {1: {'sentenceId': 1, 'id': 1, 'tokens': [1, 2], 'root': 1}, 2: {'sentenceId': 1, 'id': 2, 'tokens': [3, 4], 'root': 3}}), ('sentences', {1: {'id': 1, 'tokenFrom': 1, 'tokenTo': 5, 'clauses': [1, 2], 'object': [1]}}), ('paragraphs', {1: {'id': 1, 'tokens': [1, 2, 3, 4]}}), ('dependencies', [{'arcs': {1: [{'governor': 2}], 2: [{'governor': 3}]}}]), ('coreferences', [{'id': 1, 'representative': {'head': 1, 'tokens': [1, 2]}, 'referents': [{'head': 3, 'tokens': [3, 4]}]}, {'id': 2, 'representative': {'head': 1, 'tokens': [1, 2]}, 'referents': [{'head': 3, 'tokens': [3, 4]}]}, {'id': 2, 'head': 1, 'tokens': [1]}, {'id': 3}]), ('constituents', [{'sentenceId': 1}]), ('expressions', [{'id': 1, 'head': 1, 'tokens': [1]}])])
        assert expected == actual, actual

    def test_add_annotation_to_a_from_b_coreferences(self):
        unifier = Unifier()
        a = build_json()
        b = build_json()
        b['coreferences'].append({'id': 2})
        actual = unifier.add_annotation_to_a_from_b(a, b, 'coreferences')
        expected = OrderedDict([('tokenList', {1: {'id': 1, 'text': 'a'}, 2: {'id': 2, 'text': 'b'}, 3: {'id': 3, 'text': 'c'}, 4: {'id': 4, 'text': 'd'}}), ('clauses', {1: {'sentenceId': 1, 'id': 1, 'tokens': [1, 2], 'root': 1}, 2: {'sentenceId': 1, 'id': 2, 'tokens': [3, 4], 'root': 3}}), ('sentences', {1: {'id': 1, 'tokenFrom': 1, 'tokenTo': 5, 'clauses': [1, 2], 'object': [1]}}), ('paragraphs', {1: {'id': 1, 'tokens': [1, 2, 3, 4]}}), ('dependencies', [{'arcs': {1: [{'governor': 2}], 2: [{'governor': 3}]}}]), ('coreferences', [{'id': 1, 'representative': {'head': 1, 'tokens': [1, 2]}, 'referents': [{'head': 3, 'tokens': [3, 4]}]}, {'id': 2, 'representative': {'head': 1, 'tokens': [1, 2]}, 'referents': [{'head': 3, 'tokens': [3, 4]}]}, {'id': 3, 'representative': {'head': 1, 'tokens': [1, 2]}, 'referents': [{'head': 3, 'tokens': [3, 4]}]}, {'id': 5, 'representative': {'head': 1, 'tokens': [1, 2]}, 'referents': [{'head': 3, 'tokens': [3, 4]}]}, {'id': 6}]), ('constituents', [{'sentenceId': 1}]), ('expressions', [{'id': 1, 'head': 1, 'tokens': [1]}])])
        assert expected == actual, actual

    def test_add_annotation_to_a_from_b_tokens(self):
        unifier = Unifier()
        a = build_json()
        b = build_json()
        b['tokenList'][1]['new'] = 1
        b['tokenList'][1]['new_dict'] = {'a': 1}
        a['tokenList'][1]['dict'] = {'a': 1}
        b['tokenList'][1]['dict'] = {'a': 1}
        b['tokenList'][1]['dict']['b'] = 2
        a['tokenList'][1]['dict']['c'] = 3
        actual = unifier.add_annotation_to_a_from_b(a, b, 'tokens')
        expected = OrderedDict([('tokenList', {1: {'id': 1, 'text': 'a', 'dict': {'a': 1, 'c': 3, 'b': 2}, 'new': 1, 'new_dict': {'a': 1}}, 2: {'id': 2, 'text': 'b'}, 3: {'id': 3, 'text': 'c'}, 4: {'id': 4, 'text': 'd'}}), ('clauses', {1: {'sentenceId': 1, 'id': 1, 'tokens': [1, 2], 'root': 1}, 2: {'sentenceId': 1, 'id': 2, 'tokens': [3, 4], 'root': 3}}), ('sentences', {1: {'id': 1, 'tokenFrom': 1, 'tokenTo': 5, 'clauses': [1, 2], 'object': [1]}}), ('paragraphs', {1: {'id': 1, 'tokens': [1, 2, 3, 4]}}), ('dependencies', [{'arcs': {1: [{'governor': 2}], 2: [{'governor': 3}]}}]), ('coreferences', [{'id': 1, 'representative': {'head': 1, 'tokens': [1, 2]}, 'referents': [{'head': 3, 'tokens': [3, 4]}]}, {'id': 2, 'representative': {'head': 1, 'tokens': [1, 2]}, 'referents': [{'head': 3, 'tokens': [3, 4]}]}]), ('constituents', [{'sentenceId': 1}]), ('expressions', [{'id': 1, 'head': 1, 'tokens': [1]}])])
        assert expected == actual, actual

    def test_extend_a_with_b(self):
        unifier = Unifier()
        a = build_json()
        b = build_json()
        actual = unifier.extend_a_with_b(a, b)
        expected = OrderedDict([('tokenList', {1: {'id': 1, 'text': 'a'}, 2: {'id': 2, 'text': 'b'}, 3: {'id': 3, 'text': 'c'}, 4: {'id': 4, 'text': 'd'}, 5: {'id': 5, 'text': 'a'}, 6: {'id': 6, 'text': 'b'}, 7: {'id': 7, 'text': 'c'}, 8: {'id': 8, 'text': 'd'}}), ('clauses', {1: {'sentenceId': 1, 'id': 1, 'tokens': [1, 2], 'root': 1}, 2: {'sentenceId': 1, 'id': 2, 'tokens': [3, 4], 'root': 3}, 3: {'sentenceId': 2, 'id': 3, 'tokens': [5, 6], 'root': 5}, 4: {'sentenceId': 2, 'id': 4, 'tokens': [7, 8], 'root': 7}}), ('sentences', {1: {'id': 1, 'tokenFrom': 1, 'tokenTo': 5, 'clauses': [1, 2], 'object': [1]}, 2: {'id': 2, 'tokenFrom': 5, 'tokenTo': 9, 'clauses': [3, 4], 'object': [5]}}), ('paragraphs', {1: {'id': 1, 'tokens': [1, 2, 3, 4]}, 2: {'id': 2, 'tokens': [5, 6, 7, 8]}}), ('dependencies', [{'arcs': {1: [{'governor': 2}], 2: [{'governor': 3}]}}, {'arcs': {9: [{'governor': 10}], 10: [{'governor': 11}]}}]), ('coreferences', [{'id': 1, 'representative': {'head': 1, 'tokens': [1, 2]}, 'referents': [{'head': 3, 'tokens': [3, 4]}]}, {'id': 2, 'representative': {'head': 1, 'tokens': [1, 2]}, 'referents': [{'head': 3, 'tokens': [3, 4]}]}, {'id': 3, 'representative': {'head': 5, 'tokens': [5, 6]}, 'referents': [{'head': 7, 'tokens': [7, 8]}]}, {'id': 4, 'representative': {'head': 5, 'tokens': [5, 6]}, 'referents': [{'head': 7, 'tokens': [7, 8]}]}]), ('constituents', [{'sentenceId': 1}, {'sentenceId': 2}]), ('expressions', {'id': 2, 'head': 5, 'tokens': [5]})])
        assert expected == actual, actual

    def test_extend_a_with_b_no_side_effects(self):
        unifier = Unifier()
        a = build_json()
        b = build_json()
        a_copy = OrderedDict(a)
        b_copy = OrderedDict(b)
        unifier.extend_a_with_b(a, b)
        assert a_copy == a, a
        assert b_copy == b, b
