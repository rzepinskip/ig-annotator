import pandas as pd
from igannotator.annotator import MultiparserAnnotator
import os

statute_df = pd.read_csv("data/RegulaminSejmuRzeczypospolitej.csv")
counter = 1
for index, row in statute_df.iterrows():
    example = row.Content
    print(example)

    annotator = MultiparserAnnotator()
    dfs = annotator.annotate(example)
    for df in dfs:
        if df.empty:
            continue
        print(df)

        directory = './conllu/maltparser'
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(directory + '/maltparser' + str(counter) + '.conllu', 'w+') as f:
            df.to_csv(f, sep="\t", header=False)
        counter += 1
