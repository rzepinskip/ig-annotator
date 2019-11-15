import requests
import json
import pandas as pd
from io import StringIO

statute_df = pd.read_csv("data/RegulaminSejmuRzeczypospolitej.csv")
example = statute_df.iloc[16].Content
print(example)

url = "http://ws.clarin-pl.eu/nlprest2/base/process"
parameters = {
    "lpmn": 'any2txt|wcrft2|dependpar|out("conll_")|out("svg_")',
    "text": example,
    "application": "ws.clarin-pl.eu",
    "user": "demo",
}

payload = json.dumps(parameters)
headers = {
    "Content-Type": "text/html; charset=utf-8",
    "cache-control": "no-cache",
}

response = requests.request("POST", url, data=payload, headers=headers)

# CoNLL-X format - http://anthology.aclweb.org/W/W06/W06-2920.pdf
# (https://universaldependencies.org/format.html)
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

dfs = list()
for sentence in response.text.split("\n\n"):
    df = pd.read_csv(StringIO(sentence), sep="\t", header=None, names=cols).set_index(
        "id"
    )
    dfs.append(df)

dfs[0]

# TODO display tree
