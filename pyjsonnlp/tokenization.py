from typing import List

import syntok.segmenter as segmenter
from syntok.tokenizer import Token


class ConllToken(Token):
    def __init__(self, space_prefix: str, value: str, offset: int):
        super(ConllToken, self).__init__(space_prefix=space_prefix, value=value, offset=offset)
        self._space_after = False

    @property
    def space_after(self) -> bool:
        return self._space_after

    @space_after.setter
    def space_after(self, value: bool):
        self._space_after = value


def segment(text: str) -> List[List[ConllToken]]:
    sentences = []
    for paragraph in segmenter.process(text):
        for sentence in paragraph:
            sent: List[ConllToken] = []
            sentences.append(sent)
            for i, token in enumerate(sentence):
                sent.append(ConllToken(space_prefix=token.spacing, value=token.value, offset=token.offset))
                if i > 0:
                    sent[-2].space_after = sent[-1].spacing == ' '

    return sentences
