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
    """
    Converts JSON-NLP to CoNLL-U (no enhanced dependencies, coref, or ner)
    Baseline functionality is for Xrenner to be able to use spaCy dependencies to do coref
    """
    c = ""
    #for d in j['documents'].values():
    for d in j['documents']:
        c = f"{c}# newdoc id = {d['id']}\n"
        token_offset = 0
        for s in d['sentences'].values():
            c = f"{c}# sent id = {s['id']}\n"
            tl = d['tokenList']
            i = 0
            for t_id in range(s['tokenFrom'], s['tokenTo']):
                i += 1
                head, rel = get_dep_head_rel(d, t_id)
                text = tl[t_id-1].get('text')
                # spacy pronoun "lemmas"
                lemma = tl[t_id-1].get('lemma', '_') if tl[t_id-1].get('lemma', '_') != '-PRON-' else text
                c = f"{c}{t_id-token_offset}" \
                    f"\t{text}" \
                    f"\t{lemma.lower()}" \
                    f"\t{tl[t_id].get('upos', tl[t_id].get('xpos', '_'))}" \
                    f"\t{tl[t_id].get('xpos', '_')}" \
                    f"\t{encode_features(tl[t_id].get('features', {}))}" \
                    f"\t{max(0, head-token_offset)}" \
                    f"\t{rel}" \
                    f"\t_\t_\n"
            c = f"{c}\n"
            token_offset += i

    return c.rstrip()


def get_dep_head_rel(d: OrderedDict, t_id: int) -> Tuple[int, str]:
    """For a given token, return its head and arc label"""
    for deps in d.get('dependencies', []):
        if deps.get('style', 'universal') == 'universal' and t_id in deps['arcs'].keys():
            arc = deps['arcs'][t_id][0]
            return arc['governor'], arc['label']
    return 0, '_'  # defaults


def parse_conllu(c: str, dependency_arc_style='universal') -> OrderedDict:
    """
    Convert CoNLL-U format to NLP-JSON
    # todo detect contractions, head, expression types
    # todo reconstruct sentence text
    # todo syntax, coref, and other conllu-plus columns
    # todo test par/sent/doc ids and par splitting
    """
    par_num = 1
    doc_num = 1

    def new_paragraph_mid_sentence():
        nonlocal par_num
        # if an opening paragraph wasn't specified, retroactively create one
        if not document['paragraphs']:
            conll_id = sent.metadata.get('newpar id', '')
            document['paragraphs'][par_num] = {
                'id': par_num,
                'conllId': conll_id,
                'tokens': [t_id+1 for t_id in range(len(document['tokenList']))]
            }
            par_num += 1
        # create the new paragraph
        document['paragraphs'][par_num] = {
            'id': par_num,
            'tokens': []
        }
        par_num += 1

    def wrap_up_doc():
        if all(map(lambda ds: 'text' in ds, document['sentences'].values())):
            document['text'] = ' '.join(map(lambda ds: ds['text'], document['sentences'].values()))
        #j['documents'][document['id']] = document
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
            document = get_base_document(doc_num)
            document['conllId'] = sent.metadata.get('newdoc id', '')
            doc_num += 1

        # paragraphs
        if 'newpar id' in sent.metadata or 'newpar' in sent.metadata:
            document['paragraphs'][par_num] = {
                'id': par_num,
                'conllId': sent.metadata.get('newpar id', ''),
                'tokens': []}
            par_num += 1

        # initialize a sentence
        if 'sent_id' in sent.metadata:
            j['conll']['sentence_ids'] = True
        sent_tokens: List[int] = []
        current_sent = {
            'id': sent_num,
            'conllId': sent.metadata.get('sent_id', ''),
            'tokenFrom': token_id,
            'tokenTo': token_id + len(sent),
            'tokens': sent_tokens
        }
        document['sentences'][sent_num] = current_sent

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
                if token.get('misc', defaultdict()).get('NewPar') == True:
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
                    'Overt': True
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
                if t['misc'].get('NewPar') == True:
                    new_paragraph_mid_sentence()

            # non-overt tokens are represented as decimal ids in conll
            if '.' in str_token_id:
                t['features']['Overt'] = False

            # bookkeeping
            token_lookup[(sent_num, str_token_id)] = token_id
            current_sent['tokens'].append(token_id)
            if document['paragraphs']:
                document['paragraphs'][par_num]['tokens'].append('token_id')
            #document['tokenList'][token_id] = t
            document['tokenList'].append(t)
            token_id += 1

        # expressions (now we handle id ranges)
        expr_id = 1
        for token in sent:
            if isinstance(token['id'], tuple) and token['id'][1] == '-':
                document['expressions'].append({
                    'id': expr_id,
                    'type': 'conll-range',
                    'tokens': [token_lookup[(sent_num, str(t))] for t in range(token['id'][0], token['id'][2] + 1)]
                })
                expr_id += 1

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
                            'label': rel.lower(),
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


def encode_features(features: dict) -> str:
    """Encodes features from a dictionary/JSON to CONLLU format."""

    return '|'.join(map(lambda kv: f'{kv[0]}={kv[1]}', features.items())) if features else '_'
