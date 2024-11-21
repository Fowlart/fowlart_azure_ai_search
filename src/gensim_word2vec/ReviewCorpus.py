from gensim.test.utils import datapath
from gensim import utils

class ReviewCorpus:
    """An iterator that yields sentences (lists of str)."""

    def __iter__(self) -> list[str]:
        corpus_path = datapath('lee_background.cor')
        for line in open(corpus_path):
            # assume there's one document per line, tokens separated by whitespace
            yield utils.simple_preprocess(line)