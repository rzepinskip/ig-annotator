from os import listdir
import pathlib
import pandas as pd
import click
from igannotator.annotator.word import LexicalTree, annotate_df
from igannotator.rulesexecutor.rules_executor import IGRulesExecutor


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
def annotate_files(directory):
    executor = IGRulesExecutor()

    for input in listdir(directory):
        file_path = pathlib.Path(directory) / pathlib.Path(input)
        # if input != "stanford1.conllu":
        #     continue
        if file_path.is_file() and file_path.suffix == ".conllu":
            with open(file_path, "r+") as input:
                df = pd.read_csv(input, sep="\t", header=None)
                tree = annotate_df(df)
                tags = executor.execute(tree)
                print(tree.show_children_subtrees())

            for tag in tags:
                print(f"{tag.tag_name}: {tag.words}")

            with open(file_path.with_suffix(".xml"), "w") as output:
                output.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
                output.write("<ADICO_test_1>\n")

                sentence = ""
                for x in tree.get_all_descendants():
                    sentence += (
                        " " + x.value if x.tag != "PUNCT" and x.id != 1 else x.value
                    )
                output.write(f"<TEXT><![CDATA[{sentence}]]></TEXT>\n")

                output.write("<TAGS>\n")
                id = 0
                tag_names = {
                    "IGElement.AIM": "aIm",
                    "IGElement.ATTRIBUTE": "Attribute",
                    "IGElement.OBJECT": "oBject",
                    "IGElement.SEPARATOR": "SEPARATOR",
                    "IGElement.DEONTIC": "Deontic",
                }
                for tag in tags:
                    words = [x[1] for x in sorted(tag.words, key=lambda x: x[0])]
                    start = sentence.find(words[0])
                    stop = sentence.find(words[-1]) + len(words[-1])
                    spans = f"{start}~{stop}"
                    output.write(
                        f'<{tag_names[str(tag.tag_name)]} id="x{id}" spans="{spans}" text="{sentence[start:stop]}" />\n'
                    )
                    id += 1
                output.write("</TAGS>\n")

                output.write("</ADICO_test_1>")


if __name__ == "__main__":
    annotate_files()

