from collections import OrderedDict
from unittest import TestCase

from pyjsonnlp.dependencies import UniversalDependencyParse
from pyjsonnlp.tokenization import surface_string

j = OrderedDict({
  "meta": {
    "DC.conformsTo": "0.2.9",
    "DC.created": "2019-04-25T20:31:28",
    "DC.date": "2019-04-25T20:31:28"
  },
  "documents": {
    1: {
      "meta": {
        "DC.conformsTo": "0.2.9",
        "DC.source": "SpaCy 2.1.3",
        "DC.created": "2019-04-25T20:31:28",
        "DC.date": "2019-04-25T20:31:28",
        "DC.language": "en"
      },
      "id": 1,
      "text": "I want to buy a big red car.",
      "tokenList": OrderedDict({
        1: {
          "id": 1,
          "text": "I",
          "lemma": "-PRON-",
          "xpos": "PRP",
          "upos": "PRON",
          "entity_iob": "O",
          "characterOffsetBegin": 0,
          "characterOffsetEnd": 1,
          "lang": "en",
          "features": {
            "Overt": "Yes",
            "Stop": "Yes",
            "Alpha": "Yes",
            "PronType": "Prs",
            "Foreign": "No"
          },
          "misc": {
            "SpaceAfter": "Yes"
          },
          "shape": "X"
        },
        2: {
          "id": 2,
          "text": "want",
          "lemma": "want",
          "xpos": "VBP",
          "upos": "VERB",
          "entity_iob": "O",
          "characterOffsetBegin": 2,
          "characterOffsetEnd": 6,
          "lang": "en",
          "features": {
            "Overt": "Yes",
            "Stop": "No",
            "Alpha": "Yes",
            "VerbForm": "Fin",
            "Tense": "Pres",
            "Foreign": "No"
          },
          "misc": {
            "SpaceAfter": "Yes"
          },
          "shape": "xxxx"
        },
        3: {
          "id": 3,
          "text": "to",
          "lemma": "to",
          "xpos": "TO",
          "upos": "PART",
          "entity_iob": "O",
          "characterOffsetBegin": 7,
          "characterOffsetEnd": 9,
          "lang": "en",
          "features": {
            "Overt": "Yes",
            "Stop": "Yes",
            "Alpha": "Yes",
            "PartType": "Inf",
            "VerbForm": "Inf",
            "Foreign": "No"
          },
          "misc": {
            "SpaceAfter": "Yes"
          },
          "shape": "xx"
        },
        4: {
          "id": 4,
          "text": "buy",
          "lemma": "buy",
          "xpos": "VB",
          "upos": "VERB",
          "entity_iob": "O",
          "characterOffsetBegin": 10,
          "characterOffsetEnd": 13,
          "lang": "en",
          "features": {
            "Overt": "Yes",
            "Stop": "No",
            "Alpha": "Yes",
            "VerbForm": "Inf",
            "Foreign": "No"
          },
          "misc": {
            "SpaceAfter": "Yes"
          },
          "shape": "xxx"
        },
        5: {
          "id": 5,
          "text": "a",
          "lemma": "a",
          "xpos": "DT",
          "upos": "DET",
          "entity_iob": "O",
          "characterOffsetBegin": 14,
          "characterOffsetEnd": 15,
          "lang": "en",
          "features": {
            "Overt": "Yes",
            "Stop": "Yes",
            "Alpha": "Yes",
            "Foreign": "No"
          },
          "misc": {
            "SpaceAfter": "Yes"
          },
          "shape": "x"
        },
        6: {
          "id": 6,
          "text": "big",
          "lemma": "big",
          "xpos": "JJ",
          "upos": "ADJ",
          "entity_iob": "O",
          "characterOffsetBegin": 16,
          "characterOffsetEnd": 19,
          "lang": "en",
          "features": {
            "Overt": "Yes",
            "Stop": "No",
            "Alpha": "Yes",
            "Degree": "Pos",
            "Foreign": "No"
          },
          "misc": {
            "SpaceAfter": "Yes"
          },
          "shape": "xxx"
        },
        7: {
          "id": 7,
          "text": "red",
          "lemma": "red",
          "xpos": "JJ",
          "upos": "ADJ",
          "entity_iob": "O",
          "characterOffsetBegin": 20,
          "characterOffsetEnd": 23,
          "lang": "en",
          "features": {
            "Overt": "Yes",
            "Stop": "No",
            "Alpha": "Yes",
            "Degree": "Pos",
            "Foreign": "No"
          },
          "misc": {
            "SpaceAfter": "Yes"
          },
          "shape": "xxx"
        },
        8: {
          "id": 8,
          "text": "car",
          "lemma": "car",
          "xpos": "NN",
          "upos": "NOUN",
          "entity_iob": "O",
          "characterOffsetBegin": 24,
          "characterOffsetEnd": 27,
          "lang": "en",
          "features": {
            "Overt": "Yes",
            "Stop": "No",
            "Alpha": "Yes",
            "Number": "Sing",
            "Foreign": "No"
          },
          "misc": {
            "SpaceAfter": "No"
          },
          "shape": "xxx"
        },
        9: {
          "id": 9,
          "text": ".",
          "lemma": ".",
          "xpos": ".",
          "upos": "PUNCT",
          "entity_iob": "O",
          "characterOffsetBegin": 27,
          "characterOffsetEnd": 28,
          "lang": "en",
          "features": {
            "Overt": "Yes",
            "Stop": "No",
            "Alpha": "No",
            "PunctType": "Peri",
            "Foreign": "No"
          },
          "misc": {
            "SpaceAfter": "No"
          }
        }
      }),
      "sentences": {
        1: {
          "id": 1,
          "tokenFrom": 1,
          "tokenTo": 10,
          "tokens": [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9
          ]
        }
      },
      "dependencies": [
        {
          "style": "universal",
          "arcs": {
            1: [
              {
                "sentenceId": 1,
                "label": "nsubj",
                "governor": 2,
                "dependent": 1
              }
            ],
            2: [
              {
                "sentenceId": 1,
                "label": "root",
                "governor": 0,
                "dependent": 2
              }
            ],
            3: [
              {
                "sentenceId": 1,
                "label": "aux",
                "governor": 4,
                "dependent": 3
              }
            ],
            4: [
              {
                "sentenceId": 1,
                "label": "xcomp",
                "governor": 2,
                "dependent": 4
              }
            ],
            5: [
              {
                "sentenceId": 1,
                "label": "det",
                "governor": 8,
                "dependent": 5
              }
            ],
            6: [
              {
                "sentenceId": 1,
                "label": "amod",
                "governor": 8,
                "dependent": 6
              }
            ],
            7: [
              {
                "sentenceId": 1,
                "label": "amod",
                "governor": 8,
                "dependent": 7
              }
            ],
            8: [
              {
                "sentenceId": 1,
                "label": "dobj",
                "governor": 4,
                "dependent": 8
              }
            ],
            9: [
              {
                "sentenceId": 1,
                "label": "punct",
                "governor": 2,
                "dependent": 9
              }
            ]
          }
        }
      ],
      "constituents": [
        {
          "sentenceId": 1,
          "labeledBracketing": "(ROOT (S (NP (PRP I)) (VP (VBP want) (S (VP (TO to) (VP (VB buy) (NP (DT a) (JJ big) (JJ red) (NN car)))))) (. .)))"
        }
      ],
      "expressions": [
        {
          "id": 1,
          "type": "NP",
          "head": 8,
          "dependency": "dobj",
          "tokens": [
            5,
            6,
            7,
            8
          ]
        }
      ]
    }
  }
})


class TestUniversalDependencies(TestCase):
    def setUp(self) -> None:
        self.d = UniversalDependencyParse(j['documents'][1]['dependencies'][0], j['documents'][1]['tokenList'])

    def test_get_leaves_all(self):
        actual = surface_string(self.d.get_leaves(2))
        expected = 'I want to buy a big red car.'
        assert expected == actual, actual

    def test_get_leaves_np(self):
        actual = surface_string(self.d.get_leaves(8))
        expected = 'a big red car'
        assert expected == actual, actual

    def test_get_leaves_multi_branches(self):
        actual = surface_string(self.d.get_leaves(4))
        expected = 'to buy a big red car'
        assert expected == actual, actual

    def test_get_leaves_by_arc_xcomp(self):
        head, arcs = self.d.get_leaves_by_arc('xcomp')
        actual = surface_string(arcs)
        expected = 'to buy a big red car'
        assert expected == actual, actual
        assert 4 == head, head

    def test_get_leaves_by_arc_dobj(self):
        head, arcs = self.d.get_leaves_by_arc('dobj')
        actual = surface_string(arcs)
        expected = 'a big red car'
        assert expected == actual, actual
        assert 8 == head, head

    def test_get_leaves_by_arc_amod(self):
        head, arcs = self.d.get_leaves_by_arc('amod')
        actual = surface_string(arcs, trim=True)
        expected = 'red'
        assert expected == actual, actual
        assert 7 == head, head

    def test_is_arc_present_below(self):
        assert self.d.is_arc_present_below(2, 'xcomp')
        assert not self.d.is_arc_present_below(2, 'fake')
        assert not self.d.is_arc_present_below(4, 'xcomp')

    def test_get_child_with_arc(self):
        actual = self.d.get_child_with_arc(2, 'nsubj')
        expected = {'id': 1, 'text': 'I', 'lemma': '-PRON-', 'xpos': 'PRP', 'upos': 'PRON', 'entity_iob': 'O', 'characterOffsetBegin': 0, 'characterOffsetEnd': 1, 'lang': 'en', 'features': {'Overt': 'Yes', 'Stop': 'Yes', 'Alpha': 'Yes', 'PronType': 'Prs', 'Foreign': 'No'}, 'misc': {'SpaceAfter': 'Yes'}, 'shape': 'X'}
        assert expected == actual, actual
        assert not self.d.get_child_with_arc(2, 'fake')
        


