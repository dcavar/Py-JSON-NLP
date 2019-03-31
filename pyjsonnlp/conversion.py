#!/usr/bin/env python3

"""
(C) 2019 Oren Baldinger

Functions for converting to and from CoNNL-U format

Licensed under the Apache License 2.0, see the file LICENSE for more details.

Brought to you by the NLP-Lab.org (https://nlp-lab.org/)!
"""
from collections import OrderedDict, defaultdict
from typing import Dict, Tuple

import conllu

from pyjsonnlp import get_base, get_base_document


def to_conllu(j: OrderedDict) -> str:
    """Converts JSON-NLP to CONLLU"""
    raise NotImplementedError()
    # c = ""
    # for d in j['documents']:
    #     par_id = None
    #     c = f"{c}\n# newdoc id = {d['id']}"
    #
    #     for t in d['tokenList']:
    #         pass
    #
    # return c


def parse_conllu(c: str, dependency_arc_style='universal') -> OrderedDict:
    """
    Convert CoNLL-U format to NLP-JSON
    # todo detect contractions, head, expression types
    # todo reconstruct sentence text
    # todo syntax, coref, and other conllu-plus columns
    # todo test par/sent/doc ids and par splitting
    """

    def new_paragraph_mid_sentence():
        # if an opening paragraph wasn't specified, retroactively create one
        if not document['paragraphs']:
            document['paragraphs'].append({
                'tokens': [t_id for t_id in document['tokenList']]
            })
            if 'newpar id' in sent.metadata:
                document['paragraphs'][-1]['id'] = sent.metadata['newpar id']
        # create the new paragraph
        document['paragraphs'].append({
            'tokens': []
        })

    def wrap_up_doc():
        if all(map(lambda ds: 'text' in ds, document['sentences'])):
            document['text'] = ' '.join(map(lambda ds: ds['text'], document['sentences']))
        j['documents'].append(document)

    # init
    j: OrderedDict = get_base()
    token_lookup: Dict[Tuple[int, str], int] = {}
    token_id = 1
    document = None
    parsed = conllu.parse(c)

    # start parsing sentences
    for sent_num, sent in enumerate(parsed):
        # documents
        if 'newdoc id' in sent.metadata or 'newdoc' in sent.metadata or document is None:
            if document is not None:
                wrap_up_doc()
            document = get_base_document()
            if 'newdoc id' in sent.metadata:
                document['id'] = sent.metadata['newdoc id']

        # paragraphs
        if 'newpar id' in sent.metadata:
            document['paragraphs'].append({
                'id': str(sent.metadata.get('newpar id')),
                'tokens': []
            })
        elif 'newpar' in sent.metadata:
            document['paragraphs'].append({'tokens': []})

        # initialize a sentence
        if 'sent_id' in sent.metadata:
            j['conll']['sentence_ids'] = True
        current_sent = {
            'id': sent.metadata.get('sent_id', str(sent_num)),
            'tokenFrom': token_id,
            'tokenTo': token_id + len(sent),
            'tokens': []
        }
        document['sentences'].append(current_sent)

        # sentence text
        if 'text' in sent.metadata:
            current_sent['text'] = sent.metadata['text']

        # translations
        translations = []
        for key in sent.metadata.keys():
            if 'text_' in key:
                translations.append({
                    'lang': key[5:],
                    'text': sent.metadata[key]
                })
        if translations:
            current_sent['translations'] = translations

        # tokens
        for token in sent:
            str_token_id = str(token['id'])
            # multi-token expressions
            if '-' in str_token_id:
                # this will be in the range token, not the word itself
                if token.get('misc', defaultdict()).get('NewPar') == 'Yes':
                    new_paragraph_mid_sentence()
                # ignore ranges otherwise during token parsing
                continue

            # initialize the token
            t = {
                'id': token_id,
                'text': token['form'],
                'lemma': token['lemma'],
                'upos': token['upostag'],  # universal pos
                'xpos': token['xpostag'],  # language-specific pos
                'features': OrderedDict({
                    'Overt': 'Yes'
                })
            }
            if token.get('feats'):
                t['features'].update(token['feats'])
            if token.get('misc'):
                t['misc'] = token['misc']
                # morphemes in two places
                if 'Mseg' in t['misc']:
                    t['morphemes'] = t['misc']['Mseg'].split('-')
                # new paragraph in the middle of a sentence
                if t['misc'].get('NewPar') == 'Yes':
                    new_paragraph_mid_sentence()

            # non-overt tokens are represented as decimal ids in conll
            if '.' in str_token_id:
                t['features']['Overt'] = 'No'

            # bookkeeping
            token_lookup[(sent_num, str_token_id)] = token_id
            current_sent['tokens'].append(token_id)
            if document['paragraphs']:
                document['paragraphs'][-1].append('token_id')
            token_id += 1
            document['tokenList'].append(t)

        # expressions (now we handle id ranges)
        for token in sent:
            if isinstance(token['id'], tuple) and token['id'][1] == '-':
                document['expressions'].append({
                    'type': 'conll-range',
                    'tokens': [token_lookup[(sent_num, str(t))] for t in range(token['id'][0], token['id'][2] + 1)]
                })

    # dependencies
    for token_key, style in (('deprel', dependency_arc_style), ('deps', 'enhanced')):
        deps = {'style': style, 'arcs': {}}
        for sent_num, sent in enumerate(parsed):
            for token in sent:
                # None, '_', or not present
                if token.get(token_key, '_') == '_' or not token.get(token_key):
                    continue
                dependent = token_lookup[(sent_num, str(token['id']))]
                deps['arcs'][dependent] = []
                if token_key == 'deps':
                    for rel, head in token[token_key]:
                        deps['arcs'][dependent].append({
                            'label': rel,
                            'governor': 0 if rel.upper() == 'ROOT' else token_lookup[(sent_num, str(head))],
                            'dependent': dependent
                        })
                else:
                    deps['arcs'][dependent].append({
                        'label': token[token_key] if token[token_key] != 'ROOT' else 'root',
                        'governor': 0 if token[token_key].upper() == 'ROOT' else token_lookup[(sent_num, str(token['head']))],
                        'dependent': dependent
                    })
        if deps:
            document['dependencies'].append(deps)

    wrap_up_doc()

    return j


def _parse_features(features: str) -> dict:
    """Parses CONLLU features and splits them up into dictionaries."""

    d = OrderedDict()
    for f in features.split('|'):
        for k, v in f.split('='):
            d[k] = v
    return d


def _encode_features(features: dict) -> str:
    """Encodes features from a dictionary/JSON to CONLLU format."""

    return '|'.join(map(lambda kv: f'{kv[0]}={kv[1]}', features.items()))
