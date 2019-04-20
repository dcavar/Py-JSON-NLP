from collections import OrderedDict
from unittest import TestCase
import pyjsonnlp
import pytest
from . import mocks

j = OrderedDict([('meta', OrderedDict([('DC.conformsTo', '0.1'), ('DC.created', '2019-01-25T17:04:34'), ('DC.date', '2019-01-25T17:04:34')])), ('documents', [OrderedDict([('meta', OrderedDict([('DC.conformsTo', '0.1'), ('DC.source', 'SpaCy 2.0.12'), ('DC.created', '2019-01-25T17:04:34'), ('DC.date', '2019-01-25T17:04:34'), ('DC.language', 'en')])), ('text', 'Autonomous cars from the countryside of France shift insurance liability toward manufacturers. People are afraid that they will crash.'), ('tokenList', [{'id': 1, 'text': 'Autonomous', 'lemma': 'autonomous', 'xpos': 'JJ', 'upos': 'ADJ', 'entity_iob': 'O', 'characterOffsetBegin': 0, 'characterOffsetEnd': 10, 'lang': 'en', 'features': {'Overt': 'Yes', 'Stop': 'No', 'Alpha': 'Yes', 'Foreign': 'No'}, 'misc': {'SpaceAfter': 'Yes'}, 'shape': 'Xxxxx'}, {'id': 2, 'text': 'cars', 'lemma': 'car', 'xpos': 'NNS', 'upos': 'NOUN', 'entity_iob': 'O', 'characterOffsetBegin': 11, 'characterOffsetEnd': 15, 'lang': 'en', 'features': {'Overt': 'Yes', 'Stop': 'No', 'Alpha': 'Yes', 'Foreign': 'No'}, 'misc': {'SpaceAfter': 'Yes'}, 'shape': 'xxxx'}, {'id': 3, 'text': 'from', 'lemma': 'from', 'xpos': 'IN', 'upos': 'ADP', 'entity_iob': 'O', 'characterOffsetBegin': 16, 'characterOffsetEnd': 20, 'lang': 'en', 'features': {'Overt': 'Yes', 'Stop': 'No', 'Alpha': 'Yes', 'Foreign': 'No'}, 'misc': {'SpaceAfter': 'Yes'}, 'shape': 'xxxx'}, {'id': 4, 'text': 'the', 'lemma': 'the', 'xpos': 'DT', 'upos': 'DET', 'entity_iob': 'O', 'characterOffsetBegin': 21, 'characterOffsetEnd': 24, 'lang': 'en', 'features': {'Overt': 'Yes', 'Stop': 'No', 'Alpha': 'Yes', 'Foreign': 'No'}, 'misc': {'SpaceAfter': 'Yes'}, 'shape': 'xxx'}, {'id': 5, 'text': 'countryside', 'lemma': 'countryside', 'xpos': 'NN', 'upos': 'NOUN', 'entity_iob': 'O', 'characterOffsetBegin': 25, 'characterOffsetEnd': 36, 'lang': 'en', 'features': {'Overt': 'Yes', 'Stop': 'No', 'Alpha': 'Yes', 'Foreign': 'No'}, 'misc': {'SpaceAfter': 'Yes'}, 'shape': 'xxxx'}, {'id': 6, 'text': 'of', 'lemma': 'of', 'xpos': 'IN', 'upos': 'ADP', 'entity_iob': 'O', 'characterOffsetBegin': 37, 'characterOffsetEnd': 39, 'lang': 'en', 'features': {'Overt': 'Yes', 'Stop': 'No', 'Alpha': 'Yes', 'Foreign': 'No'}, 'misc': {'SpaceAfter': 'Yes'}, 'shape': 'xx'}, {'id': 7, 'text': 'France', 'lemma': 'france', 'xpos': 'NNP', 'upos': 'PROPN', 'entity_iob': 'B', 'characterOffsetBegin': 40, 'characterOffsetEnd': 46, 'lang': 'en', 'features': {'Overt': 'Yes', 'Stop': 'No', 'Alpha': 'Yes', 'Foreign': 'No'}, 'misc': {'SpaceAfter': 'Yes'}, 'shape': 'Xxxxx', 'entity': 'GPE'}, {'id': 8, 'text': 'shift', 'lemma': 'shift', 'xpos': 'NN', 'upos': 'NOUN', 'entity_iob': 'O', 'characterOffsetBegin': 47, 'characterOffsetEnd': 52, 'lang': 'en', 'features': {'Overt': 'Yes', 'Stop': 'No', 'Alpha': 'Yes', 'Foreign': 'No'}, 'misc': {'SpaceAfter': 'Yes'}, 'shape': 'xxxx'}, {'id': 9, 'text': 'insurance', 'lemma': 'insurance', 'xpos': 'NN', 'upos': 'NOUN', 'entity_iob': 'O', 'characterOffsetBegin': 53, 'characterOffsetEnd': 62, 'lang': 'en', 'features': {'Overt': 'Yes', 'Stop': 'No', 'Alpha': 'Yes', 'Foreign': 'No'}, 'misc': {'SpaceAfter': 'Yes'}, 'shape': 'xxxx'}, {'id': 10, 'text': 'liability', 'lemma': 'liability', 'xpos': 'NN', 'upos': 'NOUN', 'entity_iob': 'O', 'characterOffsetBegin': 63, 'characterOffsetEnd': 72, 'lang': 'en', 'features': {'Overt': 'Yes', 'Stop': 'No', 'Alpha': 'Yes', 'Foreign': 'No'}, 'misc': {'SpaceAfter': 'Yes'}, 'shape': 'xxxx'}, {'id': 11, 'text': 'toward', 'lemma': 'toward', 'xpos': 'IN', 'upos': 'ADP', 'entity_iob': 'O', 'characterOffsetBegin': 73, 'characterOffsetEnd': 79, 'lang': 'en', 'features': {'Overt': 'Yes', 'Stop': 'No', 'Alpha': 'Yes', 'Foreign': 'No'}, 'misc': {'SpaceAfter': 'Yes'}, 'shape': 'xxxx'}, {'id': 12, 'text': 'manufacturers', 'lemma': 'manufacturer', 'xpos': 'NNS', 'upos': 'NOUN', 'entity_iob': 'O', 'characterOffsetBegin': 80, 'characterOffsetEnd': 93, 'lang': 'en', 'features': {'Overt': 'Yes', 'Stop': 'No', 'Alpha': 'Yes', 'Foreign': 'No'}, 'misc': {'SpaceAfter': 'No'}, 'shape': 'xxxx'}, {'id': 13, 'text': '.', 'lemma': '.', 'xpos': '.', 'upos': 'PUNCT', 'entity_iob': 'O', 'characterOffsetBegin': 93, 'characterOffsetEnd': 94, 'lang': 'en', 'features': {'Overt': 'Yes', 'Stop': 'No', 'Alpha': 'No', 'Foreign': 'No'}, 'misc': {'SpaceAfter': 'Yes'}}, {'id': 14, 'text': 'People', 'lemma': 'people', 'xpos': 'NNS', 'upos': 'NOUN', 'entity_iob': 'O', 'characterOffsetBegin': 95, 'characterOffsetEnd': 101, 'lang': 'en', 'features': {'Overt': 'Yes', 'Stop': 'No', 'Alpha': 'Yes', 'Foreign': 'No'}, 'misc': {'SpaceAfter': 'Yes'}, 'shape': 'Xxxxx'}, {'id': 15, 'text': 'are', 'lemma': 'be', 'xpos': 'VBP', 'upos': 'VERB', 'entity_iob': 'O', 'characterOffsetBegin': 102, 'characterOffsetEnd': 105, 'lang': 'en', 'features': {'Overt': 'Yes', 'Stop': 'No', 'Alpha': 'Yes', 'Foreign': 'No'}, 'misc': {'SpaceAfter': 'Yes'}, 'shape': 'xxx'}, {'id': 16, 'text': 'afraid', 'lemma': 'afraid', 'xpos': 'JJ', 'upos': 'ADJ', 'entity_iob': 'O', 'characterOffsetBegin': 106, 'characterOffsetEnd': 112, 'lang': 'en', 'features': {'Overt': 'Yes', 'Stop': 'No', 'Alpha': 'Yes', 'Foreign': 'No'}, 'misc': {'SpaceAfter': 'Yes'}, 'shape': 'xxxx'}, {'id': 17, 'text': 'that', 'lemma': 'that', 'xpos': 'IN', 'upos': 'ADP', 'entity_iob': 'O', 'characterOffsetBegin': 113, 'characterOffsetEnd': 117, 'lang': 'en', 'features': {'Overt': 'Yes', 'Stop': 'No', 'Alpha': 'Yes', 'Foreign': 'No'}, 'misc': {'SpaceAfter': 'Yes'}, 'shape': 'xxxx'}, {'id': 18, 'text': 'they', 'lemma': '-PRON-', 'xpos': 'PRP', 'upos': 'PRON', 'entity_iob': 'O', 'characterOffsetBegin': 118, 'characterOffsetEnd': 122, 'lang': 'en', 'features': {'Overt': 'Yes', 'Stop': 'No', 'Alpha': 'Yes', 'Foreign': 'No'}, 'misc': {'SpaceAfter': 'Yes'}, 'shape': 'xxxx'}, {'id': 19, 'text': 'will', 'lemma': 'will', 'xpos': 'MD', 'upos': 'VERB', 'entity_iob': 'O', 'characterOffsetBegin': 123, 'characterOffsetEnd': 127, 'lang': 'en', 'features': {'Overt': 'Yes', 'Stop': 'No', 'Alpha': 'Yes', 'Foreign': 'No'}, 'misc': {'SpaceAfter': 'Yes'}, 'shape': 'xxxx'}, {'id': 20, 'text': 'crash', 'lemma': 'crash', 'xpos': 'VB', 'upos': 'VERB', 'entity_iob': 'O', 'characterOffsetBegin': 128, 'characterOffsetEnd': 133, 'lang': 'en', 'features': {'Overt': 'Yes', 'Stop': 'No', 'Alpha': 'Yes', 'Foreign': 'No'}, 'misc': {'SpaceAfter': 'No'}, 'shape': 'xxxx'}, {'id': 21, 'text': '.', 'lemma': '.', 'xpos': '.', 'upos': 'PUNCT', 'entity_iob': 'O', 'characterOffsetBegin': 133, 'characterOffsetEnd': 134, 'lang': 'en', 'features': {'Overt': 'Yes', 'Stop': 'No', 'Alpha': 'No', 'Foreign': 'No'}, 'misc': {'SpaceAfter': 'No'}}]), ('sentences', [{'id': '0', 'tokenFrom': 1, 'tokenTo': 14, 'tokens': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]}, {'id': '1', 'tokenFrom': 14, 'tokenTo': 22, 'tokens': [14, 15, 16, 17, 18, 19, 20, 21]}]), ('dependencies', [{'style': 'universal', 'arcs': {1: {'sentenceId': '0', 'label': 'amod', 'governor': 2, 'dependent': 1}, 2: {'sentenceId': '0', 'label': 'nsubj', 'governor': 8, 'dependent': 2}, 3: {'sentenceId': '0', 'label': 'prep', 'governor': 2, 'dependent': 3}, 4: {'sentenceId': '0', 'label': 'det', 'governor': 5, 'dependent': 4}, 5: {'sentenceId': '0', 'label': 'pobj', 'governor': 3, 'dependent': 5}, 6: {'sentenceId': '0', 'label': 'prep', 'governor': 5, 'dependent': 6}, 7: {'sentenceId': '0', 'label': 'pobj', 'governor': 6, 'dependent': 7}, 8: {'sentenceId': '0', 'label': 'root', 'governor': 0, 'dependent': 8}, 9: {'sentenceId': '0', 'label': 'compound', 'governor': 10, 'dependent': 9}, 10: {'sentenceId': '0', 'label': 'dobj', 'governor': 8, 'dependent': 10}, 11: {'sentenceId': '0', 'label': 'prep', 'governor': 8, 'dependent': 11}, 12: {'sentenceId': '0', 'label': 'pobj', 'governor': 11, 'dependent': 12}, 13: {'sentenceId': '0', 'label': 'punct', 'governor': 8, 'dependent': 13}, 14: {'sentenceId': '1', 'label': 'nsubj', 'governor': 15, 'dependent': 14}, 15: {'sentenceId': '1', 'label': 'root', 'governor': 0, 'dependent': 15}, 16: {'sentenceId': '1', 'label': 'acomp', 'governor': 15, 'dependent': 16}, 17: {'sentenceId': '1', 'label': 'mark', 'governor': 20, 'dependent': 17}, 18: {'sentenceId': '1', 'label': 'nsubj', 'governor': 20, 'dependent': 18}, 19: {'sentenceId': '1', 'label': 'aux', 'governor': 20, 'dependent': 19}, 20: {'sentenceId': '1', 'label': 'ccomp', 'governor': 16, 'dependent': 20}, 21: {'sentenceId': '1', 'label': 'punct', 'governor': 15, 'dependent': 21}}}]), ('coreferences', [{'id': 0, 'representative': {'tokens': [14], 'head': 14}, 'referents': [{'tokens': [14], 'head': 14}, {'tokens': [18], 'head': 18}]}]), ('expressions', [{'type': 'NP', 'head': 2, 'dependency': 'nsubj', 'tokens': [1, 2, 3]}, {'type': 'NP', 'head': 5, 'dependency': 'pobj', 'tokens': [4, 5, 6]}, {'type': 'NP', 'head': 10, 'dependency': 'dobj', 'tokens': [9, 10]}])])])])


class TestJsonNlpConstruction(TestCase):
    def test_get_base(self):
        pyjsonnlp.__version__ = 0.1
        actual = pyjsonnlp.get_base()
        expected = OrderedDict([('meta', {'DC.conformsTo': 0.1, 'DC.source': '', 'DC.created': '2019-01-25T17:04:34', 'DC.date': '2019-01-25T17:04:34', 'DC.creator': '', 'DC.publisher': '', 'DC.title': '', 'DC.description': '', 'DC.identifier': '', 'DC.language': '', 'DC.subject': '', 'DC.contributors': '', 'DC.type': '', 'DC.format': '', 'DC.relation': '', 'DC.coverage': '', 'DC.rights': '', 'counts': {}}), ('conll', {}), ('documents', {})])
        assert actual == expected, actual

    def test_get_base_document(self):
        pyjsonnlp.__version__ = 0.1
        actual = pyjsonnlp.get_base_document(2)
        expected = OrderedDict([('meta', {'DC.conformsTo': 0.1, 'DC.source': '', 'DC.created': '2019-01-25T17:04:34', 'DC.date': '2019-01-25T17:04:34', 'DC.creator': '', 'DC.publisher': '', 'DC.title': '', 'DC.description': '', 'DC.identifier': '', 'DC.language': '', 'DC.subject': '', 'DC.contributors': '', 'DC.type': '', 'DC.format': '', 'DC.relation': '', 'DC.coverage': '', 'DC.rights': '', 'counts': {}}), ('id', 2), ('conllId', ''), ('text', ''), ('tokenList', {}), ('clauses', {}), ('sentences', {}), ('paragraphs', {}), ('dependencies', []), ('coreferences', []), ('constituents', []), ('expressions', [])])
        assert actual == expected, actual

    def test_build_coreference(self):
        actual = pyjsonnlp.build_coreference(42)
        expected = {'id': 42, 'representative': {'tokens': []}, 'referents': []}
        assert expected == actual, actual

    def test_build_constituents(self):
        actual = pyjsonnlp.build_constituents(0, "(NN text)")
        expected = {'sentenceId': 0, 'labeledBracketing': '(ROOT (NN text))'}
        assert expected == actual, actual

    def test_build_constituents_with_root(self):
        actual = pyjsonnlp.build_constituents(0, "[ROOT [NN text]]")
        expected = {'sentenceId': 0, 'labeledBracketing': '[ROOT [NN text]]'}
        assert expected == actual, actual


class TestJsonNLPManipulation(TestCase):
    def test_remove_empty_fields(self):
        d = OrderedDict([('a', 1), ('b', ''), ('c', []), ('d', [1, 2])])
        d['meta'] = OrderedDict([('a', 1), ('b', ''), ('c', {}), ('d', [1, 2])])
        d['documents'] = {
            1: OrderedDict([('a', 1), ('b', ''), ('c', []), ('d', [1, 2])]),
            2: OrderedDict([('a', 1), ('b', ''), ('c', {}), ('d', [1, 2])])
        }
        actual = pyjsonnlp.remove_empty_fields(d)
        expected = OrderedDict([('a', 1), ('d', [1, 2]), ('meta', OrderedDict([('a', 1), ('d', [1, 2])])), ('documents', {1: OrderedDict([('a', 1), ('d', [1, 2])]), 2: OrderedDict([('a', 1), ('d', [1, 2])])})])
        assert expected == actual, actual

    def test_find_head(self):
        token_ids = [1]
        doc = OrderedDict({
            'dependencies': [{
                'style': 'universal',
                'arcs': {
                    1: [{'governor': 2}],
                    2: [{'governor': 3}],
                    3: [{'governor': 4}],
                    4: [{'governor': 0}],
                    5: [{'governor': 4}],
                }
            }]
        })
        actual = pyjsonnlp.find_head(doc, token_ids, 'universal')
        assert 1 == actual, actual

    def test_find_head_style_not_found(self):
        no_deps = OrderedDict(j['documents'][0])
        no_deps['dependencies'] = []
        with pytest.raises(ValueError):
            pyjsonnlp.find_head(no_deps, [], 'no such style')

    def test_find_head_long_phrases(self):
        token_ids = [x for x in range(1, 6)]
        doc = OrderedDict({
            'dependencies': [{
                'style': 'universal',
                'arcs': {
                    1: [{'governor': 2}],
                    2: [{'governor': 3}],
                    3: [{'governor': 4}],
                    4: [{'governor': 0}],
                    5: [{'governor': 4}],
                }
            }]
        })
        actual = pyjsonnlp.find_head(doc, token_ids, 'universal')
        assert 4 == actual, actual

    def test_find_head_no_enhanced(self):
        with pytest.raises(ValueError):
            pyjsonnlp.find_head(OrderedDict(), [], 'Enhanced++')

    def test_find_head_no_deps(self):
        no_deps = OrderedDict(j['documents'][0])
        no_deps['dependencies'] = []
        with pytest.raises(ValueError):
            pyjsonnlp.find_head(no_deps, [], 'universal')
