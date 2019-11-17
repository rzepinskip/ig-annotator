from abc import ABC, abstractmethod


class BaseAnnotator(ABC):
    @abstractmethod
    def annotate(self, text: str):
        raise NotImplementedError()
