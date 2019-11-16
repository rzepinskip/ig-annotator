import pandas as pd
from igannotator.annotator import MultiparserAnnotator

statute_df = pd.read_csv("data/RegulaminSejmuRzeczypospolitej.csv")
example = statute_df.iloc[16].Content
print(example)


annotator = MultiparserAnnotator()
dfs = annotator.annotate(example)
print(dfs[0])
