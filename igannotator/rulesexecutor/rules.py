from abc import ABC, abstractmethod
from ..annotator.word import Word
from enum import Enum


class IGElement(Enum):
    AIM = 1
    ATTRIBUTE = 2
    OBJECT = 3
    SEPARATOR = 4
    DEONTIC = 5


class Rule(ABC):
    @abstractmethod
    def apply(self, tree: Word) -> Word:
        raise NotImplementedError()


class DeonticIfWordFromDictionary(Rule):
    def apply(self, tree: Word):
        if tree.lemm in ["musieć", "móc"]:
            tree.ig_tag = IGElement.DEONTIC


class RootIsAimRule(Rule):
    def apply(self, tree: Word):
        if tree.relation == "root" and tree.ig_tag is None:
            tree.ig_tag = IGElement.AIM


class NsubjFromAimIsAttributeRule(Rule):
    def apply(self, tree: Word):
        if tree.ig_tag != IGElement.AIM:
            return

        for c in tree.children:
            if c.relation == "nsubj":
                c.ig_tag = IGElement.ATTRIBUTE


class NsubjFromAimIsAttributeRule(Rule):
    def apply(self, tree: Word):
        if tree.ig_tag != IGElement.AIM:
            return

        for c in tree.children:
            if c.relation == "nsubj":
                c.ig_tag = IGElement.ATTRIBUTE


class ObjsFromAimAreObjects(Rule):
    def apply(self, tree: Word):
        if tree.ig_tag != IGElement.AIM:
            return

        for c in tree.children:
            if c.relation in ["obj", "dobj", "obl"]:
                c.ig_tag = IGElement.OBJECT


class PunctFromAimIsSeparator(Rule):
    def apply(self, tree: Word):
        if tree.ig_tag != IGElement.AIM:
            return

        for c in tree.children:
            if c.relation == "punct":
                c.ig_tag = IGElement.SEPARATOR
