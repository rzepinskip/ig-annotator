import json
import requests
import pandas as pd
from io import StringIO
from .annotator import BaseAnnotator


class MultiparserAnnotator(BaseAnnotator):
    def _get_base_url(self):
        return "http://ws.clarin-pl.eu/nlprest2/base/process"

    def _create_headers(self):
        return {
            "Content-Type": "text/html; charset=utf-8",
            "cache-control": "no-cache",
        }

    def _create_payload(self, text: str):
        parameters = {
            "lpmn": 'any2txt|wcrft2|dependpar|out("conll_")|out("svg_")',
            "text": text,
            "application": "ws.clarin-pl.eu",
            "user": "demo",
        }
        return json.dumps(parameters)

    def _send_request(self, text: str):
        headers = self._create_headers()
        payload = self._create_payload(text)
        return requests.request(
            "POST", url=self._get_base_url(), data=payload, headers=headers
        )

    def _sentence_to_df(self, sentence: str):
        cols = [
            "id",
            "form",
            "lemma",
            "cpostag",
            "postag",
            "feats",
            "head",
            "deprel",
            "phead",
            "pdeprel",
        ]
        return pd.read_csv(
            StringIO(sentence), sep="\t", header=None, names=cols
        ).set_index("id")

    def _parse_response(self, response):
        # CoNLL-X format - http://anthology.aclweb.org/W/W06/W06-2920.pdf
        # (https://universaldependencies.org/format.html)
        dfs = [
            self._sentence_to_df(sentence) for sentence in response.text.split("\n\n")
        ]
        return dfs

    def annotate(self, text: str):
        response = self._send_request(text)
        return self._parse_response(response)
