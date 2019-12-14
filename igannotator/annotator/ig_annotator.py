import pandas as pd
from typing import List, Tuple
from igannotator.annotator.annotator import BaseAnnotator
from igannotator.annotator.lexical_tree import LexcialTreeNode
from igannotator.rulesexecutor.rules import IGTag
from igannotator.annotator import StanfordAnnotator
import stanfordnlp
from igannotator.rulesexecutor.rules_executor import IGRulesExecutor
from igannotator.annotator.preprocessing import split_text_into_sentence, remove_dots


class IgAnnotator(BaseAnnotator):
    def __init__(self):
        super().__init__()
        RESOURCES_DIR = "resources"

        stanfordnlp.download(
            "pl", resource_dir=RESOURCES_DIR, confirm_if_exists=False, force=True
        )
        self._stanford_annotator = StanfordAnnotator(RESOURCES_DIR)
        self._executor = IGRulesExecutor()

    def annotate(self, text: str) -> List[Tuple[LexcialTreeNode, List[IGTag]]]:
        sentences = split_text_into_sentence(text)

        return [self._annotate_sentence(x) for x in sentences]

    def _annotate_sentence(self, sentence: str) -> Tuple[LexcialTreeNode, List[IGTag]]:
        processed_sentence = remove_dots(sentence)

        dfs = self._stanford_annotator.annotate(processed_sentence)
        if len(dfs) != 1:
            print(dfs)
            raise ValueError(f"Incorrect input data: {sentence}")

        tree = LexcialTreeNode.from_conllu_df(dfs[0])
        tags = self._executor.execute(tree)

        return (tree, tags)

