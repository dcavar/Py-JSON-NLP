from unittest import TestCase

from pyjsonnlp.tokenization import ConllToken, segment

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
