from os import listdir
from os.path import isfile, join
import pandas as pd
from igannotator.annotator.word import LexicalTree, annotate_df
from igannotator.rulesexecutor.rules_executor import IGRulesExecutor


def annotate_file(file_path):
    with open(file_path, 'r+') as f:
        df = pd.read_csv(f, sep="\t", header=None)

    id_to_word = dict()
    for index, row in df.iterrows():
        word = LexicalTree(row)
        id_to_word[word.id] = word

    root = None
    for word in id_to_word.values():
        if word.parent == 0:
            root = word
            continue
        id_to_word[word.parent].children.append(word)

    print(root.show_children_subtrees())

    return root


directory = "conllu/goldStandard-stanford"

executor =IGRulesExecutor()

for f in listdir(directory):
    file_path = join(directory, f)
    if isfile(file_path):
        with open(file_path, 'r+') as f:
            df = pd.read_csv(f, sep="\t", header=None)
            tree = annotate_df(df)
            tags = executor.execute(tree)
            print(tree.show_children_subtrees())
            print(tags)




