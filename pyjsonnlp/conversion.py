#!/usr/bin/env python3

"""
(C) 2019 Oren Baldinger

Functions for converting to and from CoNNL-U format

Licensed under the Apache License 2.0, see the file LICENSE for more details.

Brought to you by the NLP-Lab.org (https://nlp-lab.org/)!
"""
from collections import OrderedDict, defaultdict
from typing import Dict, Tuple, List

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
    par_num = 1
    new_par_id = None
    doc_num = 1

    def new_paragraph_mid_sentence():
        nonlocal new_par_id, par_num
        # if an opening paragraph wasn't specified, retroactively create one
        if not document['paragraphs']:
            new_par_id = str(sent.metadata.get('newpar id', par_num))
            document['paragraphs'][new_par_id] = {
                'id': new_par_id,
                'tokens': [t_id for t_id in document['tokenList'].keys()]
            }
            par_num += 1
        # create the new paragraph
        new_par_id = str(par_num)
        document['paragraphs'][new_par_id] = {
            'id': new_par_id,
            'tokens': []
        }
        par_num += 1

    def wrap_up_doc():
        if all(map(lambda ds: 'text' in ds, document['sentences'])):
            document['text'] = ' '.join(map(lambda ds: ds['text'], document['sentences']))
        j['documents'][document['id']] = document

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
            new_doc_id = sent.metadata['newdoc id'] if 'newdoc id' in sent.metadata else str(doc_num)
            doc_num += 1
            document = get_base_document(new_doc_id)

        # paragraphs
        if 'newpar id' in sent.metadata or 'newpar' in sent.metadata:
            new_par_id = str(sent.metadata.get('newpar id', par_num))
            document['paragraphs'][new_par_id] = {'id': new_par_id, 'tokens': []}
            par_num += 1

        # initialize a sentence
        if 'sent_id' in sent.metadata:
            j['conll']['sentence_ids'] = True
        new_sent_id = sent.metadata.get('sent_id', str(sent_num))
        sent_tokens: List[int] = []
        current_sent = {
            'id': new_sent_id,
            'tokenFrom': token_id,
            'tokenTo': token_id + len(sent),
            'tokens': sent_tokens
        }
        document['sentences'][new_sent_id] = current_sent

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
                document['paragraphs'][new_par_id]['tokens'].append('token_id')
            document['tokenList'][token_id] = t
            token_id += 1

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
