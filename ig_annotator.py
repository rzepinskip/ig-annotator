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


def get_sentence_and_tags(tree, tags):
    sentence = ""
    id_to_position = dict()
    for x in tree.get_all_descendants():
        if x.tag != "PUNCT" and x.id != 1:
            id_to_position[x.id] = len(sentence) + 1
            sentence += " " + x.value
        else:
            id_to_position[x.id] = len(sentence)
            sentence += x.value

    tag_names = {
        "IGElement.AIM": "aIm",
        "IGElement.ATTRIBUTE": "Attribute",
        "IGElement.OBJECT": "oBject",
        "IGElement.ACTOR": "aCtor",
        "IGElement.SEPARATOR": "SEPARATOR",
        "IGElement.DEONTIC": "Deontic",
    }

    tags_tuples = list()
    for tag in tags:
        words_with_ids = sorted(tag.words, key=lambda x: x[0])
        start = id_to_position[words_with_ids[0][0]]
        stop = id_to_position[words_with_ids[-1][0]] + len(words_with_ids[-1][1])
        tags_tuples.append(
            (tag_names[str(tag.tag_name)], start, stop, sentence[start:stop])
        )

    print(f"{sentence}: {tags}")
    return (sentence, tags_tuples)


def write_mae(output_file, trees_with_tags):
    sentences_with_tags = [
        get_sentence_and_tags(tree, tags) for tree, tags in trees_with_tags
    ]

    with open(output_file, "w", encoding="utf-8") as output:
        output.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
        output.write("<ADICO_test_1>\n")

        text = "\n".join([sentence for sentence, _ in sentences_with_tags])
        output.write(f"<TEXT><![CDATA[{text}]]></TEXT>\n")

        output.write("<TAGS>\n")

        offset = 0
        id = 0
        for sentence, tags in sentences_with_tags:
            for tag_name, start, stop, tag_text in tags:
                spans = f"{offset + start}~{offset + stop}"
                tag_repr = f'<{tag_name} id="x{id}" spans="{spans}" text="{sentence[start:stop]}" />\n'
                output.write(tag_repr)
                id += 1
            offset += len(sentence) + 1

        output.write("</TAGS>\n")

        output.write("</ADICO_test_1>")


@click.command()
@click.argument("directory", type=click.Path(exists=True))
@click.argument("output", type=click.Path(exists=False))
def annotate_files(directory, output):
    executor = IGRulesExecutor()

    mae_data = list()
    subset = list(listdir(directory))
    for input in subset[:6]:
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

    write_mae("tmp.xml", mae_data)


if __name__ == "__main__":
    annotate_files()

