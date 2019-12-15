import pandas as pd
import stanfordnlp
import os
import re

from igannotator.annotator import IgAnnotator
from igannotator.output.mae import write_mae_representation

RESOURCES_DIR = "resources"

annotator = IgAnnotator(RESOURCES_DIR)

directory = "data/conllu/goldStandard-stanford"
if not os.path.exists(directory):
    os.makedirs(directory)

with open("data/nauka_1.txt", "r+", encoding="utf8") as input_file:
    content = input_file.read()

lines = [line for line in content.split("\n\n") if not line.startswith("--")]

mae_data = list()
for line in lines:
    line_regex = re.compile("^([0-9]*)\\. ((?s).*)$")
    regex_result = line_regex.search(line)

    if regex_result is not None:
        number = regex_result.group(1)
        sentence = regex_result.group(2)
    else:
        raise ValueError("Incorrrect format")

    tree, tags = annotator.annotate(sentence)

    mae_data.append((tree, tags))

write_mae_representation("data/goldStandard-annotated.xml", mae_data)
