from igannotator.annotator.word import LexicalTree
from typing import List
from igannotator.rulesexecutor.rules import AimExtension, AimIsXcompFromDeonticRoot, NsubjIsAttribute, ObjsFromAimAreObjects, OneRootIsAimOrDeontic, PunctFromAimIsSeparator, Rule




class RulesExecutor():
    def __init__(self, rules: List[Rule]):
        self._rules = rules

    def execute(self, tree: LexicalTree) -> LexicalTree:
        annotations = []
        for r in self._rules:
            r.apply(tree, annotations) 
        return [ann for ann in annotations if ann is not None]



class IGRulesExecutor(RulesExecutor):
    def __init__(self):
        super().__init__([OneRootIsAimOrDeontic(), AimIsXcompFromDeonticRoot(), AimExtension(
        ),NsubjIsAttribute(), ObjsFromAimAreObjects(), PunctFromAimIsSeparator()])
