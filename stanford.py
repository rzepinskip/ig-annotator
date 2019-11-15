import stanfordnlp
import pandas as pd
from io import StringIO

MODELS_DIR = "./resources"

stanfordnlp.download("pl", resource_dir=MODELS_DIR, confirm_if_exists=False, force=True)

config = {
    "processors": "tokenize,pos,lemma,depparse",
    "lang": "pl",
    "models_dir": MODELS_DIR,
}
nlp = stanfordnlp.Pipeline(**config)
example = """
Do projektu nie stosuje się przepisów o terminie wniesienia i doręczenia projektów. 
Projekt uchwały rozpatruje się w jednym czytaniu.
"""
doc = nlp(example)

doc.sentences[0].print_tokens()
doc.sentences[0].print_dependencies()

conll = doc.conll_file.conll_as_string()
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

dfs = list()
for sentence in conll.split("\n\n"):
    df = pd.read_csv(StringIO(sentence), sep="\t", header=None, names=cols).set_index(
        "id"
    )
    dfs.append(df)

dfs[0]
