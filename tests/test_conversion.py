from collections import OrderedDict
from unittest import TestCase

from pyjsonnlp import conversion
from . import mocks
import pyjsonnlp

pyjsonnlp.__version__ = "0.2.2"


class TestConllu(TestCase):
    def test_to_conllu(self):
        pass

    def test_parse_conllu(self):
        text = """1	John	John	NNP	NNP	_	2	nsubj	_	_
        2	visited	visit	VBD	VBD	_	0	ROOT	_	_
        3	Spain	Spain	NNP	NNP	_	2	dobj	_	_
        4	.	.	.	.	_	2	punct	_	_

        1	His	he	PRP$	PRP$	_	2	nmod:poss	_	_
        2	visit	visit	NN	NN	_	3	nsubj	_	_
        3	went	go	VBD	VBD	_	0	ROOT	_	_
        4	well	well	RB	RB	_	3	advmod	_	_
        5	.	.	.	.	_	3	punct	_	_"""
        actual = conversion.parse_conllu(text)
        expected = OrderedDict([('meta', {'DC.conformsTo': '0.2.2', 'DC.source': '', 'DC.created': '2019-01-25T17:04:34', 'DC.date': '2019-01-25T17:04:34', 'DC.creator': '', 'DC.publisher': '', 'DC.title': '', 'DC.description': '', 'DC.identifier': '', 'DC.language': '', 'DC.subject': '', 'DC.contributors': '', 'DC.type': '', 'DC.format': '', 'DC.relation': '', 'DC.coverage': '', 'DC.rights': '', 'counts': {}}), ('conll', {}), ('documents', {'1': OrderedDict([('meta', {'DC.conformsTo': '0.2.2', 'DC.source': '', 'DC.created': '2019-01-25T17:04:34', 'DC.date': '2019-01-25T17:04:34', 'DC.creator': '', 'DC.publisher': '', 'DC.title': '', 'DC.description': '', 'DC.identifier': '', 'DC.language': '', 'DC.subject': '', 'DC.contributors': '', 'DC.type': '', 'DC.format': '', 'DC.relation': '', 'DC.coverage': '', 'DC.rights': '', 'counts': {}}), ('id', '1'), ('text', ''), ('tokenList', {1: {'id': 1, 'text': 'John', 'lemma': 'John', 'upos': 'NNP', 'xpos': 'NNP', 'features': OrderedDict([('Overt', 'Yes')])}, 2: {'id': 2, 'text': 'visited', 'lemma': 'visit', 'upos': 'VBD', 'xpos': 'VBD', 'features': OrderedDict([('Overt', 'Yes')])}, 3: {'id': 3, 'text': 'Spain', 'lemma': 'Spain', 'upos': 'NNP', 'xpos': 'NNP', 'features': OrderedDict([('Overt', 'Yes')])}, 4: {'id': 4, 'text': '.', 'lemma': '.', 'upos': '.', 'xpos': '.', 'features': OrderedDict([('Overt', 'Yes')])}, 5: {'id': 5, 'text': 'His', 'lemma': 'he', 'upos': 'PRP$', 'xpos': 'PRP$', 'features': OrderedDict([('Overt', 'Yes')])}, 6: {'id': 6, 'text': 'visit', 'lemma': 'visit', 'upos': 'NN', 'xpos': 'NN', 'features': OrderedDict([('Overt', 'Yes')])}, 7: {'id': 7, 'text': 'went', 'lemma': 'go', 'upos': 'VBD', 'xpos': 'VBD', 'features': OrderedDict([('Overt', 'Yes')])}, 8: {'id': 8, 'text': 'well', 'lemma': 'well', 'upos': 'RB', 'xpos': 'RB', 'features': OrderedDict([('Overt', 'Yes')])}, 9: {'id': 9, 'text': '.', 'lemma': '.', 'upos': '.', 'xpos': '.', 'features': OrderedDict([('Overt', 'Yes')])}}), ('clauses', {}), ('sentences', {'0': {'id': '0', 'tokenFrom': 1, 'tokenTo': 5, 'tokens': [1, 2, 3, 4]}, '1': {'id': '1', 'tokenFrom': 5, 'tokenTo': 10, 'tokens': [5, 6, 7, 8, 9]}}), ('paragraphs', {}), ('dependencies', [{'style': 'universal', 'arcs': {1: [{'label': 'nsubj', 'governor': 2, 'dependent': 1}], 2: [{'label': 'root', 'governor': 0, 'dependent': 2}], 3: [{'label': 'dobj', 'governor': 2, 'dependent': 3}], 4: [{'label': 'punct', 'governor': 2, 'dependent': 4}], 5: [{'label': 'nmod:poss', 'governor': 6, 'dependent': 5}], 6: [{'label': 'nsubj', 'governor': 7, 'dependent': 6}], 7: [{'label': 'root', 'governor': 0, 'dependent': 7}], 8: [{'label': 'advmod', 'governor': 7, 'dependent': 8}], 9: [{'label': 'punct', 'governor': 7, 'dependent': 9}]}}, {'style': 'enhanced', 'arcs': {}}]), ('coreferences', []), ('constituents', []), ('expressions', [])])})])
        assert expected == actual, actual

    def test_conllu2json_enhanced_dependencies(self):
        text = """1    They     they    PRON    PRP    Case=Nom|Number=Plur               2    nsubj    2:nsubj|4:nsubj
2    buy      buy     VERB    VBP    Number=Plur|Person=3|Tense=Pres    0    root     0:root
3    and      and     CONJ    CC     _                                  4    cc       4:cc
3.1    they    they    PRON    PRP    _    _    _     4:nsbj|1:elip
4    sell     sell    VERB    VBP    Number=Plur|Person=3|Tense=Pres    2    conj     0:root|2:conj
5    books    book    NOUN    NNS    Number=Plur                        2    obj      2:obj|4:obj
6    .        .       PUNCT   .      _                                  2    punct    2:punct"""
        actual = conversion.parse_conllu(text)
        expected = OrderedDict([('meta', {'DC.conformsTo': '0.2.2', 'DC.source': '', 'DC.created': '2019-01-25T17:04:34', 'DC.date': '2019-01-25T17:04:34', 'DC.creator': '', 'DC.publisher': '', 'DC.title': '', 'DC.description': '', 'DC.identifier': '', 'DC.language': '', 'DC.subject': '', 'DC.contributors': '', 'DC.type': '', 'DC.format': '', 'DC.relation': '', 'DC.coverage': '', 'DC.rights': '', 'counts': {}}), ('conll', {}), ('documents', {'1': OrderedDict([('meta', {'DC.conformsTo': '0.2.2', 'DC.source': '', 'DC.created': '2019-01-25T17:04:34', 'DC.date': '2019-01-25T17:04:34', 'DC.creator': '', 'DC.publisher': '', 'DC.title': '', 'DC.description': '', 'DC.identifier': '', 'DC.language': '', 'DC.subject': '', 'DC.contributors': '', 'DC.type': '', 'DC.format': '', 'DC.relation': '', 'DC.coverage': '', 'DC.rights': '', 'counts': {}}), ('id', '1'), ('text', ''), ('tokenList', {1: {'id': 1, 'text': 'They', 'lemma': 'they', 'upos': 'PRON', 'xpos': 'PRP', 'features': OrderedDict([('Overt', 'Yes'), ('Case', 'Nom'), ('Number', 'Plur')])}, 2: {'id': 2, 'text': 'buy', 'lemma': 'buy', 'upos': 'VERB', 'xpos': 'VBP', 'features': OrderedDict([('Overt', 'Yes'), ('Number', 'Plur'), ('Person', '3'), ('Tense', 'Pres')])}, 3: {'id': 3, 'text': 'and', 'lemma': 'and', 'upos': 'CONJ', 'xpos': 'CC', 'features': OrderedDict([('Overt', 'Yes')])}, 4: {'id': 4, 'text': 'they', 'lemma': 'they', 'upos': 'PRON', 'xpos': 'PRP', 'features': OrderedDict([('Overt', 'No')])}, 5: {'id': 5, 'text': 'sell', 'lemma': 'sell', 'upos': 'VERB', 'xpos': 'VBP', 'features': OrderedDict([('Overt', 'Yes'), ('Number', 'Plur'), ('Person', '3'), ('Tense', 'Pres')])}, 6: {'id': 6, 'text': 'books', 'lemma': 'book', 'upos': 'NOUN', 'xpos': 'NNS', 'features': OrderedDict([('Overt', 'Yes'), ('Number', 'Plur')])}, 7: {'id': 7, 'text': '.', 'lemma': '.', 'upos': 'PUNCT', 'xpos': '.', 'features': OrderedDict([('Overt', 'Yes')])}}), ('clauses', {}), ('sentences', {'0': {'id': '0', 'tokenFrom': 1, 'tokenTo': 8, 'tokens': [1, 2, 3, 4, 5, 6, 7]}}), ('paragraphs', {}), ('dependencies', [{'style': 'universal', 'arcs': {1: [{'label': 'nsubj', 'governor': 2, 'dependent': 1}], 2: [{'label': 'root', 'governor': 0, 'dependent': 2}], 3: [{'label': 'cc', 'governor': 5, 'dependent': 3}], 5: [{'label': 'conj', 'governor': 2, 'dependent': 5}], 6: [{'label': 'obj', 'governor': 2, 'dependent': 6}], 7: [{'label': 'punct', 'governor': 2, 'dependent': 7}]}}, {'style': 'enhanced', 'arcs': {1: [{'label': 'nsubj', 'governor': 2, 'dependent': 1}, {'label': 'nsubj', 'governor': 5, 'dependent': 1}], 2: [{'label': 'root', 'governor': 0, 'dependent': 2}], 3: [{'label': 'cc', 'governor': 5, 'dependent': 3}], 4: [{'label': 'nsbj', 'governor': 5, 'dependent': 4}, {'label': 'elip', 'governor': 1, 'dependent': 4}], 5: [{'label': 'root', 'governor': 0, 'dependent': 5}, {'label': 'conj', 'governor': 2, 'dependent': 5}], 6: [{'label': 'obj', 'governor': 2, 'dependent': 6}, {'label': 'obj', 'governor': 5, 'dependent': 6}], 7: [{'label': 'punct', 'governor': 2, 'dependent': 7}]}}]), ('coreferences', []), ('constituents', []), ('expressions', [])])})])
        assert expected == actual, actual

    def test_conllu2json_features(self):
        text = """1    Då      då     ADV      AB                    _
2    var     vara   VERB     VB.PRET.ACT           Tense=Past|Voice=Act
3    han     han    PRON     PN.UTR.SIN.DEF.NOM    Case=Nom|Definite=Def|Gender=Com|Number=Sing
4    elva    elva   NUM      RG.NOM                Case=Nom|NumType=Card
5    år      år     NOUN     NN.NEU.PLU.IND.NOM    Case=Nom|Definite=Ind|Gender=Neut|Number=Plur
6    .       .      PUNCT    DL.MAD                _"""
        actual = conversion.parse_conllu(text)
        expected = OrderedDict([('meta', {'DC.conformsTo': '0.2.2', 'DC.source': '', 'DC.created': '2019-01-25T17:04:34', 'DC.date': '2019-01-25T17:04:34', 'DC.creator': '', 'DC.publisher': '', 'DC.title': '', 'DC.description': '', 'DC.identifier': '', 'DC.language': '', 'DC.subject': '', 'DC.contributors': '', 'DC.type': '', 'DC.format': '', 'DC.relation': '', 'DC.coverage': '', 'DC.rights': '', 'counts': {}}), ('conll', {}), ('documents', {'1': OrderedDict([('meta', {'DC.conformsTo': '0.2.2', 'DC.source': '', 'DC.created': '2019-01-25T17:04:34', 'DC.date': '2019-01-25T17:04:34', 'DC.creator': '', 'DC.publisher': '', 'DC.title': '', 'DC.description': '', 'DC.identifier': '', 'DC.language': '', 'DC.subject': '', 'DC.contributors': '', 'DC.type': '', 'DC.format': '', 'DC.relation': '', 'DC.coverage': '', 'DC.rights': '', 'counts': {}}), ('id', '1'), ('text', ''), ('tokenList', {1: {'id': 1, 'text': 'Då', 'lemma': 'då', 'upos': 'ADV', 'xpos': 'AB', 'features': OrderedDict([('Overt', 'Yes')])}, 2: {'id': 2, 'text': 'var', 'lemma': 'vara', 'upos': 'VERB', 'xpos': 'VB.PRET.ACT', 'features': OrderedDict([('Overt', 'Yes'), ('Tense', 'Past'), ('Voice', 'Act')])}, 3: {'id': 3, 'text': 'han', 'lemma': 'han', 'upos': 'PRON', 'xpos': 'PN.UTR.SIN.DEF.NOM', 'features': OrderedDict([('Overt', 'Yes'), ('Case', 'Nom'), ('Definite', 'Def'), ('Gender', 'Com'), ('Number', 'Sing')])}, 4: {'id': 4, 'text': 'elva', 'lemma': 'elva', 'upos': 'NUM', 'xpos': 'RG.NOM', 'features': OrderedDict([('Overt', 'Yes'), ('Case', 'Nom'), ('NumType', 'Card')])}, 5: {'id': 5, 'text': 'år', 'lemma': 'år', 'upos': 'NOUN', 'xpos': 'NN.NEU.PLU.IND.NOM', 'features': OrderedDict([('Overt', 'Yes'), ('Case', 'Nom'), ('Definite', 'Ind'), ('Gender', 'Neut'), ('Number', 'Plur')])}, 6: {'id': 6, 'text': '.', 'lemma': '.', 'upos': 'PUNCT', 'xpos': 'DL.MAD', 'features': OrderedDict([('Overt', 'Yes')])}}), ('clauses', {}), ('sentences', {'0': {'id': '0', 'tokenFrom': 1, 'tokenTo': 7, 'tokens': [1, 2, 3, 4, 5, 6]}}), ('paragraphs', {}), ('dependencies', [{'style': 'universal', 'arcs': {}}, {'style': 'enhanced', 'arcs': {}}]), ('coreferences', []), ('constituents', []), ('expressions', [])])})])
        assert expected == actual, actual

    def test_conllu2json_misc(self):
        text = """1     He        he        PRON    PRP     Case=Nom|Number=Sing|Person=3     2   nsubj   _   _
2     is        be        VERB    VBZ     Number=Sing|Person=3|Tense=Pres   0   root    _   _
3     in        in        ADP     IN      _                                 6   case    _   _
4     the       the       DET     DT      Definite=Def|PronType=Art         6   det     _   _
5     United    unite     VERB    VBD     Tense=Past|VerbForm=Part          6   amod    _   _
6     Kingdom   kingdom   NOUN    NN      Number=Sing                       2   nmod    _   _
7     (         (         PUNCT   -LRB-   _                                 8   punct   _   SpaceAfter=No
8     UK        UK        PROPN   NNP     Number=Sing                       6   appos   _   SpaceAfter=No
9     )         )         PUNCT   -RRB-   _                                 8   punct   _   SpaceAfter=No
10    .         .         PUNCT   .       _                                 2   punct   _   _"""
        actual = conversion.parse_conllu(text)
        expected = OrderedDict([('meta', {'DC.conformsTo': '0.2.2', 'DC.source': '', 'DC.created': '2019-01-25T17:04:34', 'DC.date': '2019-01-25T17:04:34', 'DC.creator': '', 'DC.publisher': '', 'DC.title': '', 'DC.description': '', 'DC.identifier': '', 'DC.language': '', 'DC.subject': '', 'DC.contributors': '', 'DC.type': '', 'DC.format': '', 'DC.relation': '', 'DC.coverage': '', 'DC.rights': '', 'counts': {}}), ('conll', {}), ('documents', {'1': OrderedDict([('meta', {'DC.conformsTo': '0.2.2', 'DC.source': '', 'DC.created': '2019-01-25T17:04:34', 'DC.date': '2019-01-25T17:04:34', 'DC.creator': '', 'DC.publisher': '', 'DC.title': '', 'DC.description': '', 'DC.identifier': '', 'DC.language': '', 'DC.subject': '', 'DC.contributors': '', 'DC.type': '', 'DC.format': '', 'DC.relation': '', 'DC.coverage': '', 'DC.rights': '', 'counts': {}}), ('id', '1'), ('text', ''), ('tokenList', {1: {'id': 1, 'text': 'He', 'lemma': 'he', 'upos': 'PRON', 'xpos': 'PRP', 'features': OrderedDict([('Overt', 'Yes'), ('Case', 'Nom'), ('Number', 'Sing'), ('Person', '3')])}, 2: {'id': 2, 'text': 'is', 'lemma': 'be', 'upos': 'VERB', 'xpos': 'VBZ', 'features': OrderedDict([('Overt', 'Yes'), ('Number', 'Sing'), ('Person', '3'), ('Tense', 'Pres')])}, 3: {'id': 3, 'text': 'in', 'lemma': 'in', 'upos': 'ADP', 'xpos': 'IN', 'features': OrderedDict([('Overt', 'Yes')])}, 4: {'id': 4, 'text': 'the', 'lemma': 'the', 'upos': 'DET', 'xpos': 'DT', 'features': OrderedDict([('Overt', 'Yes'), ('Definite', 'Def'), ('PronType', 'Art')])}, 5: {'id': 5, 'text': 'United', 'lemma': 'unite', 'upos': 'VERB', 'xpos': 'VBD', 'features': OrderedDict([('Overt', 'Yes'), ('Tense', 'Past'), ('VerbForm', 'Part')])}, 6: {'id': 6, 'text': 'Kingdom', 'lemma': 'kingdom', 'upos': 'NOUN', 'xpos': 'NN', 'features': OrderedDict([('Overt', 'Yes'), ('Number', 'Sing')])}, 7: {'id': 7, 'text': '(', 'lemma': '(', 'upos': 'PUNCT', 'xpos': '-LRB-', 'features': OrderedDict([('Overt', 'Yes')]), 'misc': OrderedDict([('SpaceAfter', 'No')])}, 8: {'id': 8, 'text': 'UK', 'lemma': 'UK', 'upos': 'PROPN', 'xpos': 'NNP', 'features': OrderedDict([('Overt', 'Yes'), ('Number', 'Sing')]), 'misc': OrderedDict([('SpaceAfter', 'No')])}, 9: {'id': 9, 'text': ')', 'lemma': ')', 'upos': 'PUNCT', 'xpos': '-RRB-', 'features': OrderedDict([('Overt', 'Yes')]), 'misc': OrderedDict([('SpaceAfter', 'No')])}, 10: {'id': 10, 'text': '.', 'lemma': '.', 'upos': 'PUNCT', 'xpos': '.', 'features': OrderedDict([('Overt', 'Yes')])}}), ('clauses', {}), ('sentences', {'0': {'id': '0', 'tokenFrom': 1, 'tokenTo': 11, 'tokens': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}}), ('paragraphs', {}), ('dependencies', [{'style': 'universal', 'arcs': {1: [{'label': 'nsubj', 'governor': 2, 'dependent': 1}], 2: [{'label': 'root', 'governor': 0, 'dependent': 2}], 3: [{'label': 'case', 'governor': 6, 'dependent': 3}], 4: [{'label': 'det', 'governor': 6, 'dependent': 4}], 5: [{'label': 'amod', 'governor': 6, 'dependent': 5}], 6: [{'label': 'nmod', 'governor': 2, 'dependent': 6}], 7: [{'label': 'punct', 'governor': 8, 'dependent': 7}], 8: [{'label': 'appos', 'governor': 6, 'dependent': 8}], 9: [{'label': 'punct', 'governor': 8, 'dependent': 9}], 10: [{'label': 'punct', 'governor': 2, 'dependent': 10}]}}, {'style': 'enhanced', 'arcs': {}}]), ('coreferences', []), ('constituents', []), ('expressions', [])])})])
        assert expected == actual, actual

    def test_conllu2json_ranges(self):
        text = """1     I         I      PRON    PRP   Case=Nom|Number=Sing|Person=1     2   nsubj
2-3   haven't   _      _       _     _                                 _   _
2     have      have   VERB    VBP    Number=Sing|Person=1|Tense=Pres   0   root
3     not       not    PART    RB    Negative=Neg                      2   neg
4     a         a      DET     DT    Definite=Ind|PronType=Art         5   det
5     clue      clue   NOUN    NN    Number=Sing                       2   dobj
6     .         .      PUNCT   .     _                                 2   punct"""
        actual = conversion.parse_conllu(text)
        expected = OrderedDict([('meta', {'DC.conformsTo': '0.2.2', 'DC.source': '', 'DC.created': '2019-01-25T17:04:34', 'DC.date': '2019-01-25T17:04:34', 'DC.creator': '', 'DC.publisher': '', 'DC.title': '', 'DC.description': '', 'DC.identifier': '', 'DC.language': '', 'DC.subject': '', 'DC.contributors': '', 'DC.type': '', 'DC.format': '', 'DC.relation': '', 'DC.coverage': '', 'DC.rights': '', 'counts': {}}), ('conll', {}), ('documents', {'1': OrderedDict([('meta', {'DC.conformsTo': '0.2.2', 'DC.source': '', 'DC.created': '2019-01-25T17:04:34', 'DC.date': '2019-01-25T17:04:34', 'DC.creator': '', 'DC.publisher': '', 'DC.title': '', 'DC.description': '', 'DC.identifier': '', 'DC.language': '', 'DC.subject': '', 'DC.contributors': '', 'DC.type': '', 'DC.format': '', 'DC.relation': '', 'DC.coverage': '', 'DC.rights': '', 'counts': {}}), ('id', '1'), ('text', ''), ('tokenList', {1: {'id': 1, 'text': 'I', 'lemma': 'I', 'upos': 'PRON', 'xpos': 'PRP', 'features': OrderedDict([('Overt', 'Yes'), ('Case', 'Nom'), ('Number', 'Sing'), ('Person', '1')])}, 2: {'id': 2, 'text': 'have', 'lemma': 'have', 'upos': 'VERB', 'xpos': 'VBP', 'features': OrderedDict([('Overt', 'Yes'), ('Number', 'Sing'), ('Person', '1'), ('Tense', 'Pres')])}, 3: {'id': 3, 'text': 'not', 'lemma': 'not', 'upos': 'PART', 'xpos': 'RB', 'features': OrderedDict([('Overt', 'Yes'), ('Negative', 'Neg')])}, 4: {'id': 4, 'text': 'a', 'lemma': 'a', 'upos': 'DET', 'xpos': 'DT', 'features': OrderedDict([('Overt', 'Yes'), ('Definite', 'Ind'), ('PronType', 'Art')])}, 5: {'id': 5, 'text': 'clue', 'lemma': 'clue', 'upos': 'NOUN', 'xpos': 'NN', 'features': OrderedDict([('Overt', 'Yes'), ('Number', 'Sing')])}, 6: {'id': 6, 'text': '.', 'lemma': '.', 'upos': 'PUNCT', 'xpos': '.', 'features': OrderedDict([('Overt', 'Yes')])}}), ('clauses', {}), ('sentences', {'0': {'id': '0', 'tokenFrom': 1, 'tokenTo': 8, 'tokens': [1, 2, 3, 4, 5, 6]}}), ('paragraphs', {}), ('dependencies', [{'style': 'universal', 'arcs': {1: [{'label': 'nsubj', 'governor': 2, 'dependent': 1}], 2: [{'label': 'root', 'governor': 0, 'dependent': 2}], 3: [{'label': 'neg', 'governor': 2, 'dependent': 3}], 4: [{'label': 'det', 'governor': 5, 'dependent': 4}], 5: [{'label': 'dobj', 'governor': 2, 'dependent': 5}], 6: [{'label': 'punct', 'governor': 2, 'dependent': 6}]}}, {'style': 'enhanced', 'arcs': {}}]), ('coreferences', []), ('constituents', []), ('expressions', [{'type': 'conll-range', 'tokens': [2, 3]}])])})])
        assert expected == actual, actual

    def test_conllu2json_multiple_sentences(self):
        text = """1	John	John	NNP	NNP	_	2	compound	_	_
2	Smith	Smith	NNP	NNP	_	3	nsubj	_	_
3	visited	visit	VBD	VBD	_	0	ROOT	_	_
4	Spain	Spain	NNP	NNP	_	3	dobj	_	_
5	.	.	.	.	_	3	punct	_	_

1	His	he	PRP$	PRP$	_	2	nmod:poss	_	_
2	visit	visit	NN	NN	_	3	nsubj	_	_
3	went	go	VBD	VBD	_	0	ROOT	_	_
4	well	well	RB	RB	_	3	advmod	_	_
5	.	.	.	.	_	3	punct	_	_
"""
        actual = conversion.parse_conllu(text)
        expected = OrderedDict([('meta', {'DC.conformsTo': '0.2.2', 'DC.source': '', 'DC.created': '2019-01-25T17:04:34', 'DC.date': '2019-01-25T17:04:34', 'DC.creator': '', 'DC.publisher': '', 'DC.title': '', 'DC.description': '', 'DC.identifier': '', 'DC.language': '', 'DC.subject': '', 'DC.contributors': '', 'DC.type': '', 'DC.format': '', 'DC.relation': '', 'DC.coverage': '', 'DC.rights': '', 'counts': {}}), ('conll', {}), ('documents', {'1': OrderedDict([('meta', {'DC.conformsTo': '0.2.2', 'DC.source': '', 'DC.created': '2019-01-25T17:04:34', 'DC.date': '2019-01-25T17:04:34', 'DC.creator': '', 'DC.publisher': '', 'DC.title': '', 'DC.description': '', 'DC.identifier': '', 'DC.language': '', 'DC.subject': '', 'DC.contributors': '', 'DC.type': '', 'DC.format': '', 'DC.relation': '', 'DC.coverage': '', 'DC.rights': '', 'counts': {}}), ('id', '1'), ('text', ''), ('tokenList', {1: {'id': 1, 'text': 'John', 'lemma': 'John', 'upos': 'NNP', 'xpos': 'NNP', 'features': OrderedDict([('Overt', 'Yes')])}, 2: {'id': 2, 'text': 'Smith', 'lemma': 'Smith', 'upos': 'NNP', 'xpos': 'NNP', 'features': OrderedDict([('Overt', 'Yes')])}, 3: {'id': 3, 'text': 'visited', 'lemma': 'visit', 'upos': 'VBD', 'xpos': 'VBD', 'features': OrderedDict([('Overt', 'Yes')])}, 4: {'id': 4, 'text': 'Spain', 'lemma': 'Spain', 'upos': 'NNP', 'xpos': 'NNP', 'features': OrderedDict([('Overt', 'Yes')])}, 5: {'id': 5, 'text': '.', 'lemma': '.', 'upos': '.', 'xpos': '.', 'features': OrderedDict([('Overt', 'Yes')])}, 6: {'id': 6, 'text': 'His', 'lemma': 'he', 'upos': 'PRP$', 'xpos': 'PRP$', 'features': OrderedDict([('Overt', 'Yes')])}, 7: {'id': 7, 'text': 'visit', 'lemma': 'visit', 'upos': 'NN', 'xpos': 'NN', 'features': OrderedDict([('Overt', 'Yes')])}, 8: {'id': 8, 'text': 'went', 'lemma': 'go', 'upos': 'VBD', 'xpos': 'VBD', 'features': OrderedDict([('Overt', 'Yes')])}, 9: {'id': 9, 'text': 'well', 'lemma': 'well', 'upos': 'RB', 'xpos': 'RB', 'features': OrderedDict([('Overt', 'Yes')])}, 10: {'id': 10, 'text': '.', 'lemma': '.', 'upos': '.', 'xpos': '.', 'features': OrderedDict([('Overt', 'Yes')])}}), ('clauses', {}), ('sentences', {'0': {'id': '0', 'tokenFrom': 1, 'tokenTo': 6, 'tokens': [1, 2, 3, 4, 5]}, '1': {'id': '1', 'tokenFrom': 6, 'tokenTo': 11, 'tokens': [6, 7, 8, 9, 10]}}), ('paragraphs', {}), ('dependencies', [{'style': 'universal', 'arcs': {1: [{'label': 'compound', 'governor': 2, 'dependent': 1}], 2: [{'label': 'nsubj', 'governor': 3, 'dependent': 2}], 3: [{'label': 'root', 'governor': 0, 'dependent': 3}], 4: [{'label': 'dobj', 'governor': 3, 'dependent': 4}], 5: [{'label': 'punct', 'governor': 3, 'dependent': 5}], 6: [{'label': 'nmod:poss', 'governor': 7, 'dependent': 6}], 7: [{'label': 'nsubj', 'governor': 8, 'dependent': 7}], 8: [{'label': 'root', 'governor': 0, 'dependent': 8}], 9: [{'label': 'advmod', 'governor': 8, 'dependent': 9}], 10: [{'label': 'punct', 'governor': 8, 'dependent': 10}]}}, {'style': 'enhanced', 'arcs': {}}]), ('coreferences', []), ('constituents', []), ('expressions', [])])})])
        assert expected == actual, actual

    def test_conllu2json_sentence_ids(self):
        pass

    def test_conllu2json_doc_par_ids(self):
        pass

    def test_conllu2json_doc_par_no_ids(self):
        pass

    def test_conllu2json_newpar_mid_sentence(self):
        pass

    def test_conllu2json_coref(self):
        pass

    def test_conllu2json_syntax(self):
        pass
