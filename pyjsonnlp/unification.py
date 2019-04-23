from collections import OrderedDict
from typing import List


class Unifier(object):
    @staticmethod
    def merge_tokens(a: List[int], b: List[int]) -> List[int]:
        a.extend(b)
        return list(set(a))

    @staticmethod
    def merge_coreferences(a: List[dict], b: List[dict]) -> List[dict]:
        merged: List[dict] = []
        heads = {}
        # start by adding all coreferences from a
        for coref in a:
            heads[coref['representative']['head']] = coref
            merged.append(coref)

        for coref in b:
            # add new heads cart-blanche
            if coref['representative']['head'] not in heads:
                heads[coref['representative']['head']] = coref
                merged.append(coref)
                coref['id'] = len(heads)
            else:
                # merge representative
                a_rep = heads[coref['representative']['head']]['representative']
                for k, v in coref['representative'].items():
                    if k == 'tokens':
                        a_rep[k] = Unifier.merge_tokens(a_rep[k], v)
                    elif k not in a_rep:
                        a_rep[k] = v

                # merge references
                a_refs = dict((ref['head'], ref) for ref in heads[coref['representative']['head']]['referents'])
                for ref in coref['referents']:
                    if ref['head'] not in a_refs:
                        heads[coref['representative']['head']]['referents'].append(ref)
                    else:
                        for k, v in ref.items():
                            if k == 'tokens':
                                a_refs[ref['head']][k] = Unifier.merge_tokens(a_refs[ref['head']][k], v)
                            elif k not in a_refs[ref['head']].keys():
                                a_refs[ref['head']][k] = v

        return merged

    @staticmethod
    def __copy_docs(a: OrderedDict, b: OrderedDict):
        new_doc = OrderedDict(a)
        from_doc = OrderedDict(b)

        # verify that all token ids/texts line up exactly
        a_tokens = dict((k, {'id': v['id'], 'text': v['text']}) for k, v in a['tokenList'].items())
        b_tokens = dict((k, {'id': v['id'], 'text': v['text']}) for k, v in b['tokenList'].items())
        if a_tokens != b_tokens:
            raise UnificationError('The two documents must have identical tokenLists to unify annotations!')

        return new_doc, from_doc

    @staticmethod
    def overwrite_annotation_from_a_with_b(a: OrderedDict, b: OrderedDict, annotation: str) -> OrderedDict:
        # recursively process all documents
        if 'documents' in a and 'documents' in b:
            new_json = OrderedDict(a)
            for d_id in set(a['documents'].keys()) | set(b['documents'].keys()):
                if d_id in a['documents'] and d_id in b['documents']:
                    new_json['documents'][d_id] = Unifier.overwrite_annotation_from_a_with_b(a['documents'][d_id],
                                                                                             b['documents'][d_id],
                                                                                             annotation)
            return new_json

        new_doc, from_doc = Unifier.__copy_docs(a, b)

        if annotation == 'coreferences':
            new_doc['coreferences'] = from_doc.get('coreferences', [])
        if annotation == 'expressions':
            new_doc['expressions'] = from_doc.get('expressions', [])
        elif annotation == 'tokens':
            for ta_id, t_a in new_doc.get('tokenList', {}).items():
                Unifier._merge_b_into_a(a=t_a, b=from_doc['tokenList'][ta_id], prioritize_a=False)
        else:
            raise UnificationError("Only 'coreferences', 'tokens', and 'expressions' are currently supported!")

        return new_doc

    @staticmethod
    def add_annotation_to_a_from_b(a: OrderedDict, b: OrderedDict, annotation: str) -> OrderedDict:
        # recursively process all documents
        if 'documents' in a and 'documents' in b:
            new_json = OrderedDict(a)
            for d_id in set(a['documents'].keys()) | set(b['documents'].keys()):
                if d_id in a['documents'] and d_id in b['documents']:
                    new_json['documents'][d_id] = Unifier.add_annotation_to_a_from_b(a['documents'][d_id],
                                                                                     b['documents'][d_id],
                                                                                     annotation)
            return new_json

        new_doc, from_doc = Unifier.__copy_docs(a, b)

        if annotation == 'coreferences':
            new_doc['coreferences'] = Unifier.merge_coreferences(new_doc.get('coreferences', []),
                                                                 from_doc.get('coreferences', []))
        elif annotation == 'tokens':
            for ta_id, t_a in new_doc.get('tokenList', {}).items():
                Unifier._merge_b_into_a(a=t_a, b=from_doc['tokenList'][ta_id], prioritize_a=True)
        elif annotation == 'expressions':
            for expr in from_doc.get('expressions', []):
                expr_shift = len(a.get('expressions', []))
                if 'expressions' not in new_doc:
                    new_doc['expressions'] = []
                new_doc['expressions'].append(expr)
                expr['id'] += expr_shift
        else:
            raise UnificationError("Only 'coreferences', 'tokens', and 'expressions' are currently supported!")

        return new_doc

    @staticmethod
    def _merge_b_into_a(a: dict, b: dict, prioritize_a=True) -> None:
        """Recursively merge dict b into dict a, optionally prioritizing dict a's values"""
        for k, v in b.items():
            if k not in a:
                a[k] = v
            elif isinstance(v, dict):
                Unifier._merge_b_into_a(a[k], b[k])
            elif not prioritize_a:
                a[k] = v

    @staticmethod
    def extend_a_with_b(a: OrderedDict, b: OrderedDict) -> OrderedDict:
        # recursively process all documents
        if 'documents' in a and 'documents' in b:
            new_json = OrderedDict(a)
            for d_id in set(a['documents'].keys()) | set(b['documents'].keys()):
                if d_id in a['documents'] and d_id in b['documents']:
                    new_json['documents'][d_id] = Unifier.extend_a_with_b(a['documents'][d_id],
                                                                          b['documents'][d_id])
            return new_json

        new_doc = OrderedDict(a)
        from_doc = OrderedDict(b)
        token_shift = len(a['tokenList'])
        sent_shift = len(a.get('sentences', {}))
        clause_shift = len(a.get('clauses', {}))
        par_shift = len(a.get('paragraphs', {}))
        coref_shift = len(a.get('coreferences', []))
        expr_shift = len(a.get('expressions', []))

        # tokens
        for t_id, token in from_doc['tokenList'].items():
            new_doc['tokenList'][t_id+token_shift] = token
            token['id'] += token_shift
            
        # clauses
        for c_id, clause in from_doc.get('clauses', {}).items():
            if 'clauses' not in new_doc:
                new_doc['clauses'] = {}
            new_doc['clauses'][c_id+clause_shift] = clause

            clause['sentenceId'] += sent_shift
            clause['id'] += clause_shift

            for tokens in ('mainVerb', 'tokens', 'subject', 'object'):
                if tokens in clause:
                    clause[tokens] = [t_id+token_shift for t_id in clause[tokens]]

            for token in ('root', ):
                if token in clause:
                    clause[token] += token_shift
            
        # sentences
        for s_id, sentence in from_doc.get('sentences', {}).items():
            if 'sentences' not in new_doc:
                new_doc['sentences'] = {}
            new_doc['sentences'][s_id+sent_shift] = sentence
            sentence['id'] += sent_shift

            for tokens in ('mainVerb', 'tokens', 'subject', 'object'):
                if tokens in sentence:
                    sentence[tokens] = [t_id + token_shift for t_id in sentence[tokens]]

            for token in ('tokenFrom', 'tokenTo'):
                if token in sentence:
                    sentence[token] += token_shift

            if 'clauses' in sentence:
                sentence['clauses'] = [c_id + clause_shift for c_id in sentence['clauses']]

        # paragraphs
        for p_id, par in from_doc.get('paragraphs', {}).items():
            if 'paragraphs' not in new_doc:
                new_doc['paragraphs'] = {}
            new_doc['paragraphs'][p_id+par_shift] = par
            par['id'] += par_shift
            par['tokens'] = [t_id + token_shift for t_id in par['tokens']]

        # dependencies
        for dependencies in from_doc.get('dependencies', []):
            if 'dependencies' not in new_doc:
                new_doc['dependencies'] = []
            new_doc['dependencies'].append(dependencies)

            for dep_id, arcs in dependencies['arcs'].items():
                dependencies['arcs'][dep_id+token_shift] = arcs
                del dependencies['arcs'][dep_id]

                for arc in arcs:
                    if 'sentenceId' in arc:
                        arc['sentenceId'] += sent_shift
                    arc['governor'] += token_shift
                    if 'dependent' in arc:
                        arc['dependent'] += token_shift

        # coreferences
        for coref in from_doc.get('coreferences', []):
            if 'coreferences' not in new_doc:
                new_doc['coreferences'] = []
            new_doc['coreferences'].append(coref)
            coref['id'] += coref_shift

            coref['representative']['head'] += token_shift
            coref['representative']['tokens'] = [t_id+token_shift for t_id in coref['representative']['tokens']]

            for ref in coref['referents']:
                ref['head'] += token_shift
                ref['tokens'] = [t_id + token_shift for t_id in ref['tokens']]

        # constituents
        for phrases in from_doc.get('constituents', []):
            if 'constituents' not in new_doc:
                new_doc['constituents'] = []
            new_doc['constituents'].append(phrases)

            phrases['sentenceId'] += sent_shift

        # expressions
        for expr in from_doc.get('expressions', []):
            if 'expressions' not in new_doc:
                new_doc['expressions'] = []
            new_doc['expressions'] = expr
            if 'id' in expr:
                expr['id'] += expr_shift
            if 'head' in expr:
                expr['head'] += token_shift
            expr['tokens'] = [t_id+token_shift for t_id in expr['tokens']]
        
        return new_doc


class UnificationError(Exception):
    pass
