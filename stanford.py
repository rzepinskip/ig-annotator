import pandas as pd
from igannotator.annotator import StanfordAnnotator
import stanfordnlp
import os

RESOURCES_DIR = "resources"

stanfordnlp.download(
    "pl", resource_dir=RESOURCES_DIR, confirm_if_exists=False, force=True
)

statute_df = pd.read_csv("data/RegulaminSejmuRzeczypospolitej.csv")

directory = './conllu/stanford3'
if not os.path.exists(directory):
    os.makedirs(directory)
for index, row in statute_df.iterrows():
    example = row.Content
    print(example)
    try:
        annotator = StanfordAnnotator(RESOURCES_DIR)
        dfs = annotator.annotate(example)

        output_df = pd.DataFrame()
        for df in dfs:
            output_df = output_df.append(df)
        if output_df.empty:
            continue
        output_df = output_df.reset_index(drop=True)
        output_df.index += 1

        print(output_df)

        counter = 1
        file = directory + '/stanford' + row.Article + '-' + str(int(row.Point)) + '.conllu'
        while os.path.exists(file):
            file = directory + '/stanford' + row.Article + '-' + str(int(row.Point)) + '(' + str(counter) + ')' + '.conllu'
            counter += 1

        with open(file, 'w+') as f:
            output_df.to_csv(f, sep="\t", header=False)
    except Exception as e:
        print(e)
