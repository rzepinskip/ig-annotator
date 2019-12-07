from os import listdir
from os.path import isfile, join
import pandas as pd
from igannotator.annotator.word import Word


def annotate_file(file_path):
    with open(file_path, 'r+') as f:
        df = pd.read_csv(f, sep="\t", header=None)

    id_to_word = dict()
    for index, row in df.iterrows():
        word = Word(row)
        id_to_word[word.id] = word

    root = None
    for word in id_to_word.values():
        if word.parent == 0:
            root = word
            continue
        id_to_word[word.parent].children.append(word)

    print(root.show_children_subtrees())


directory = "conllu/goldStandard-stanford"
for f in listdir(directory):
    file_path = join(directory, f)
    if isfile(file_path):
        # try:
            annotate_file(file_path)
        # except Exception as e:
        #     print(str(e) + " in " + f)
