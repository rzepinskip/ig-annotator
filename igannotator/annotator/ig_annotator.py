import pandas as pd
from typing import List, Tuple, Optional
from igannotator.annotator.annotator import BaseAnnotator
from igannotator.annotator.lexical_tree import LexcialTreeNode
from igannotator.rulesexecutor.rules import IGTag
from igannotator.annotator import StanfordAnnotator
import stanfordnlp
from igannotator.rulesexecutor.rules_executor import IGRulesExecutor
import warnings


class IgAnnotator(BaseAnnotator):
    def __init__(self, resource_dir):
        super().__init__()

        stanfordnlp.download(
            "pl", resource_dir=resource_dir, confirm_if_exists=False, force=True
        )
        self._stanford_annotator = StanfordAnnotator(resource_dir)
        self._executor = IGRulesExecutor()

    def _preprocess(self, sentence):
        def remove_dots(x: str) -> str:
            return x.replace(".", "") + "."

        return remove_dots(sentence)

    def annotate(self, sentence: str) -> Tuple[LexcialTreeNode, List[IGTag]]:
        processed_sentence = self._preprocess(sentence)

        dfs = self._stanford_annotator.annotate(processed_sentence)
        if len(dfs) != 1:
            warnings.warn(f"Unable to annotate data: {sentence}")
            return LexcialTreeNode.from_sentence(sentence), []

        tree = LexcialTreeNode.from_conllu_df(dfs[0])
        tags = self._executor.execute(tree)

        return (tree, tags)

    def get_connlu(self, sentence: str) -> str:
        processed_sentence = self._preprocess(sentence)

        doc_response = self._stanford_annotator._annotator(sentence)
        return doc_response.conll_file.conll_as_string()
