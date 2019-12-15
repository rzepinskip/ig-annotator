from typing import List

from igannotator.annotator.lexical_tree import LexcialTreeNode
from igannotator.rulesexecutor.rules import (
    IGTag,
    AimExtension,
    AimIsXcompFromDeonticRoot,
    NsubjIsAttribute,
    ObjsFromAimAreObjects,
    OneRootIsAimOrDeontic,
    PunctFromAimIsSeparator,
    Rule,
)


class RulesExecutor:
    def __init__(self, rules: List[Rule]):
        self._rules = rules

    def execute(self, tree: LexcialTreeNode) -> List[IGTag]:
        annotations: List[IGTag] = []
        for r in self._rules:
            r.apply(tree, annotations)
        return [ann for ann in annotations if ann is not None]


class IGRulesExecutor(RulesExecutor):
    def __init__(self):
        super().__init__(
            [
                OneRootIsAimOrDeontic(),
                AimIsXcompFromDeonticRoot(),
                AimExtension(),
                NsubjIsAttribute(),
                ObjsFromAimAreObjects(),
                PunctFromAimIsSeparator(),
            ]
        )
