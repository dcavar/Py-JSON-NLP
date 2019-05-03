import json
from collections import OrderedDict
from functools import reduce
from typing import List
import asyncio
from aioify import aioify

from pyjsonnlp.annotation.relations import RelationAnnotator
from pyjsonnlp.conversion import to_conllu
# from pyjsonnlp.dependencies import DependencyAnnotator
from pyjsonnlp.pipeline import Pipeline, RemotePipeline
from pyjsonnlp.unification import Unifier


class UnifiedRemotePipeline(Pipeline):
    """
    Call multiple components and unify them, via remote microservices.
    """

    def __init__(self, base_url='https://api.linguistic.technology/'):
        super().__init__()
        self.spacy = RemotePipeline(url=base_url + 'spacy')
        self.flair = RemotePipeline(url=base_url + 'flair')
        self.xrenner = RemotePipeline(url=base_url + 'xrenner')
        self.ntlk = RemotePipeline(url=base_url + 'nltk')
        self.spacy_json = OrderedDict()
        self.xrenner_json = OrderedDict()
        self.flair_json = OrderedDict()
        self.nltk_json = OrderedDict()

    @aioify
    def process_spacy(self, text, coreferences=True, constituents=False, dependencies=True):
        self.spacy_json = self.spacy.process(text, spacy_model='en_core_web_md', constituents=constituents, coreferences=coreferences, dependencies=dependencies, expressions=False)
        # convert to conll for xrenner
        spacy_conll = to_conllu(self.spacy_json)
        # run xrenner and flair
        self.xrenner_json = self.xrenner.process_conll(conll=spacy_conll)

    @aioify
    def process_flair(self, text):
        self.flair_json = self.flair.process(text=text, use_ontonotes=False, fast=True, use_embeddings='default', expressions=True)

    @aioify
    def process_nltk(self, text):
        self.nltk_json = self.ntlk.process(text=text)

    def process(self, text='', coreferences=True, constituents=False, dependencies=True, expressions=True, **kwargs) -> OrderedDict:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.async_process(text, coreferences, constituents, dependencies))

    async def async_process(self, text='', coreferences=True, constituents=False, dependencies=True) -> OrderedDict:
        # asynchronously call pipelines
        await asyncio.gather(
            self.process_spacy(text, coreferences, constituents, dependencies),
            self.process_flair(text),
            self.process_nltk(text)
        )
        # now for unification
        unifier = Unifier()

        # overwrite with flair NER, POS, etc. (including embeddings), as well as syntax chunks
        unified = unifier.overwrite_annotation_from_a_with_b(a=self.spacy_json, b=self.flair_json, annotation='tokens')
        unified = unifier.overwrite_annotation_from_a_with_b(a=unified, b=self.flair_json, annotation='expressions')

        # add xrenner coref
        unified = unifier.add_annotation_to_a_from_b(a=unified, b=self.xrenner_json, annotation='coreferences')

        # add nltk *nets
        unified = unifier.add_annotation_to_a_from_b(a=unified, b=self.nltk_json, annotation='tokens')

        # clause_annotator = DependencyAnnotator()
        relation_extractor = RelationAnnotator()
        # linker = RelationLinker()

        # clause_annotator.annotate(unified)
        relation_extractor.annotate(unified)
        # linker.annotate(unified)

        return unified

    def process_list(self, texts: List[str],  coreferences=True, constituents=False, dependencies=True, expressions=True, **kwargs) -> OrderedDict:
        """process and merge a list of texts that belong to the same document"""
        # todo async
        return reduce(Unifier().extend_a_with_b, [self.process(text=t, coreferences=coreferences,
                                                               constituents=constituents, dependencies=dependencies,
                                                               expressions=expressions) for t in texts])


class LocalUnifiedRemotePipeline(UnifiedRemotePipeline):
    def __init__(self):
        super().__init__()
        self.spacy = RemotePipeline(url='localhost', port=5001)
        self.flair = RemotePipeline(url='localhost', port=5002)
        self.xrenner = RemotePipeline(url='localhost', port=5000)
        self.ntlk = RemotePipeline(url='localhost', port=5003)


if __name__ == "__main__":
    test_text = "The Mueller Report is a very long report. We spent a long time analyzing it. Trump wishes we didn't, but that didn't stop the intrepid NlpLab."
    pipeline = UnifiedRemotePipeline()
    j = pipeline.process(text="John likes New York City. Mary doesn't like it.")
    print(json.dumps(j['documents'][1], indent=2))
