from collections import OrderedDict
from unittest import TestCase

from pyjsonnlp.tokenization import ConllToken, segment, surface_string, subtract_tokens

test_text = """That fall, two federal agencies jointly announced that the Russian government "didn't direct recent compromises of e-mails from US persons and institutions, including US political organizations," and, " [t]hese thefts and disclosures are intended to interfere with the US election process." After the election, in late December 2016, the United States imposed sanctions on Russia for having interfered in the election. By early 2017, several congressional committees were examining Russia's interference in the election."""


class TestTokenization(TestCase):
    def test_conll_token(self):
        t = ConllToken(space_prefix=' ', value='test', offset=10)
        assert 'test' == t.value, t.value
        assert ' ' == t.spacing, t.spacing
        assert 10 == t.offset, t.offset
        assert not t.space_after
        t.space_after = True
        assert t.space_after

    def test_segment(self):
        sentences = segment(test_text)
        words = []
        spaces = []
        for sent in sentences:
            for token in sent:
                words.append(token.value)
                spaces.append(token.space_after)
        expected_words = ['That', 'fall', ',', 'two', 'federal', 'agencies', 'jointly', 'announced', 'that', 'the', 'Russian', 'government', '"', 'did', 'not', 'direct', 'recent', 'compromises', 'of', 'e', 'mails', 'from', 'US', 'persons', 'and', 'institutions', ',', 'including', 'US', 'political', 'organizations', ',', '"', 'and', ',', '"', '[', 't', ']', 'hese', 'thefts', 'and', 'disclosures', 'are', 'intended', 'to', 'interfere', 'with', 'the', 'US', 'election', 'process', '.', '"', 'After', 'the', 'election', ',', 'in', 'late', 'December', '2016', ',', 'the', 'United', 'States', 'imposed', 'sanctions', 'on', 'Russia', 'for', 'having', 'interfered', 'in', 'the', 'election', '.', 'By', 'early', '2017', ',', 'several', 'congressional', 'committees', 'were', 'examining', 'Russia', "'s", 'interference', 'in', 'the', 'election', '.']
        expected_spaces = [True, False, True, True, True, True, True, True, True, True, True, True, False, False, True, True, True, True, True, False, True, True, True, True, True, False, True, True, True, True, False, False, True, False, True, True, False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, True, True, False, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, True, True, False, True, True, True, True, True, True, False, True, True, True, True, False, False]
        assert expected_spaces == spaces, spaces
        assert expected_words == words, words

    def test_surface_string(self):
        tokens = [
            OrderedDict({'text': 'I', 'misc': {'SpaceAfter': 'No'}}),
            OrderedDict({'text': "'m", 'misc': {'SpaceAfter': 'Yes'}}),
            OrderedDict({'text': 'sending', 'misc': {'SpaceAfter': 'Yes'}}),
            OrderedDict({'text': 'an', 'misc': {'SpaceAfter': 'Yes'}}),
            OrderedDict({'text': 'e'}),
            OrderedDict({'text': '-', 'misc': {}}),
            OrderedDict({'text': 'mail', 'misc': {}}),
            OrderedDict({'text': '.'}),
        ]
        actual = surface_string(tokens)
        expected = "I'm sending an e-mail."
        assert expected == actual, actual

    def test_subtract_tokens(self):
        a = [
            OrderedDict({'id': 1}),
            OrderedDict({'id': 2}),
            OrderedDict({'id': 3}),
        ]
        b = [
            OrderedDict({'id': 2}),
            OrderedDict({'id': 3}),
            OrderedDict({'id': 4}),
        ]
        aa = list(a)
        bb = list(b)
        actual = subtract_tokens(a, b)
        expected = [OrderedDict([('id', 1)])]
        assert expected == actual, actual
        assert a == aa
        assert b == bb
        actual = subtract_tokens(a, a)
        assert [] == actual, actual
        actual = subtract_tokens([], a)
        assert [] == actual, actual
        actual = subtract_tokens(a, [])
        assert a == actual, actual
