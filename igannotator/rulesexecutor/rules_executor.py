from igannotator.rulesexecutor.rules import (
    Rule,
    RootIsAimRule,
    NsubjFromAimIsAttributeRule,
    ObjsFromAimAreObjects,
    PunctFromAimIsSeparator,
    DeonticIfWordFromDictionary
)
from igannotator.annotator.word import Word
from typing import List


class RulesExecutor():
    def __init__(self, rules: List[Rule]):
        self._rules = rules

    def execute(self, tree: Word) -> Word:
        for r in self._rules:
            r.apply(tree)

        return tree


class IGRulesExecutor(RulesExecutor):
    def __init__(self):
        super().__init__([DeonticIfWordFromDictionary(), RootIsAimRule(), NsubjFromAimIsAttributeRule(
        ), ObjsFromAimAreObjects(), PunctFromAimIsSeparator()])
