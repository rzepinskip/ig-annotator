import pandas as pd
from igannotator.annotator import StanfordAnnotator
import stanfordnlp

stanfordnlp.download("pl", confirm_if_exists=False, force=True)

statute_df = pd.read_csv("data/RegulaminSejmuRzeczypospolitej.csv")
example = statute_df.iloc[16].Content
print(example)

annotator = StanfordAnnotator()
dfs = annotator.annotate(example)

print(dfs[0])
