import pandas as pd
import stanfordnlp
from io import StringIO

from igannotator.annotator.annotator import BaseAnnotator


class StanfordAnnotator(BaseAnnotator):
    def __init__(self, resources_dir):
        self._annotator = stanfordnlp.Pipeline(**self._get_config(resources_dir))

    def _get_config(self, resources_dir):
        return {
            "models_dir": resources_dir,
            "processors": "tokenize,pos,lemma,depparse",
            "lang": "pl",
        }

    def _sentence_to_df(self, sentence: str):
        # CoNLL-U https://universaldependencies.org/format.html
        cols = [
            "id",
            "form",
            "lemma",
            "upos",
            "xpos",
            "feats",
            "head",
            "deprel",
            "deps",
            "misc",
        ]
        return pd.read_csv(StringIO(sentence), sep="\t", header=None, names=cols)

    def annotate(self, text: str):
        doc_response = self._annotator(text)
        conll_string = doc_response.conll_file.conll_as_string()
        return [
            self._sentence_to_df(sentence)
            for sentence in conll_string.split("\n\n")
            if len(sentence) > 0
        ]
