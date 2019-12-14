from os import listdir
import pathlib
import pandas as pd
import click
from igannotator.annotator.word import LexicalTree, annotate_df
from igannotator.rulesexecutor.rules_executor import IGRulesExecutor
from igannotator.output.mae import write_mae_representation


def annotate_file(file_path):
    with open(file_path, "r+") as f:
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


@click.command()
@click.argument("directory", type=click.Path(exists=True))
@click.argument("output", type=click.Path(exists=False))
def annotate_files(directory, output):
    executor = IGRulesExecutor()

    mae_data = list()
    subset = list(listdir(directory))
    for input in subset[:]:
        file_path = pathlib.Path(directory) / pathlib.Path(input)
        if file_path.is_file() and file_path.suffix == ".conllu":
            with open(file_path, "r+", encoding="utf-8") as input:
                df = pd.read_csv(input, sep="\t", header=None)
                tree = annotate_df(df)
                tags = executor.execute(tree)
                # print(tree.show_children_subtrees())

            # for tag in tags:
            #     print(f"{tag.tag_name}: {tag.words}")

            mae_data.append((tree, tags))

    write_mae_representation("tmp.xml", mae_data)


if __name__ == "__main__":
    annotate_files()

