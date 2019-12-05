import pandas as pd
from igannotator.annotator import StanfordAnnotator
import stanfordnlp
import os
import re

RESOURCES_DIR = "resources"

stanfordnlp.download(
    "pl", resource_dir=RESOURCES_DIR, confirm_if_exists=False, force=True
)
annotator = StanfordAnnotator(RESOURCES_DIR)

directory = './conllu/goldStandard-stanford'
if not os.path.exists(directory):
    os.makedirs(directory)

with open("data/nauka_1.txt", "r+", encoding="utf8") as input_file:
    content = input_file.read()
lines = [line for line in content.split('\n\n') if not line.startswith('--')]
for line in lines:
    line_regex = re.compile("^([0-9]*)\\. ((?s).*)$")
    regex_result = line_regex.search(line)
    number = regex_result.group(1)
    text = regex_result.group(2)
    print(text)
    try:
        dfs = annotator.annotate(text)

        output_df = pd.DataFrame()
        for df in dfs:
            output_df = output_df.append(df)
        if output_df.empty:
            continue
        output_df = output_df.reset_index(drop=True)
        output_df.index += 1

        print(output_df)

        counter = 1
        file = directory + '/stanford' + number + '.conllu'
        while os.path.exists(file):
            file = directory + '/stanford' + number + '(' + str(counter) + ')' + '.conllu'
            counter += 1

        with open(file, 'w+') as f:
            output_df.to_csv(f, sep="\t", header=False)
    except Exception as e:
        print(e)
