#!/usr/bin/env python3

"""
(C) 2019 Damir Cavar, Oren Baldinger, Maanvitha Gongalla, Anurag Kumar, Murali Kammili

Utility Functions for JSON-NLP for manipulating and expanding an JSON-NLP objects.


Licensed under the Apache License 2.0, see the file LICENSE for more details.


Brought to you by the NLP-Lab.org (https://nlp-lab.org/)!
"""


from collections import OrderedDict, defaultdict
from typing import List, Dict, Tuple



def find_head(j: OrderedDict, token_ids: List[int], dependency_lookup: dict = None) -> Tuple[int, dict]:
    """
    Given phrase, clause, or other group of token ids,
    use the dependency parse to find the head token
    """

    if dependency_lookup is None:
        # get the dependency parse structure
        dependencies = j['dependenciesBasic']
        if not dependencies:
            dependencies = j['dependenciesEnhanced']
        if not dependencies:
            raise ValueError('A dependency parse is necessary to find the head token!')

        dependency_lookup = deps_to_dict(dependencies, 'dependent')

    if len(token_ids) == 1:
        return token_ids[0], dependency_lookup

    token_ids = set(token_ids)  # faster lookup
    for t_id in token_ids:
        # if the governor is not in the phrase, then it is the head
        if dependency_lookup[t_id]['governor'] not in token_ids:
            return t_id, dependency_lookup

    # we want well-formed phrases
    raise ValueError('This phrase does not have a head!')


def deps_to_dict(dependencies: List[dict], by: str = 'dependent') -> Dict[int, dict]:
    """Create a dictionary of dependencies, for faster lookups"""

    if by not in ('dependent', 'governor', 'label'):
        raise ValueError('by must be one of [dependent, governor, label]')
    return dict([(d[by], d) for d in dependencies])


def token_list_to_dict(token_list: List[dict]) -> Dict[int, dict]:
    """Create a tokenList dictionary, for fast lookups"""

    return dict([(t['id'], t) for t in token_list])


def build_coreference(reference_id: int) -> dict:
    """Build a frame for a coreference structure"""

    return {
        'id': reference_id,
        'representative': {
            'tokens': []
        },
        'referents': []
    }


def build_constituents(sent_id: int, s: str) -> dict:
    """ """
    s = s.rstrip().lstrip()
    open_bracket = s[0]  # ( or [
    close_bracket = s[-1]  # ) or ]
    return {
        'sent_id': sent_id,
        'labeledBracketing': f'{open_bracket}ROOT {s}{close_bracket}' if s[1:5] != 'ROOT' else s
    }
