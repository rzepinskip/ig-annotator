from collections import defaultdict
from igannotator.annotator.word import LexicalTree
from igannotator.rulesexecutor.rules import IGTag
from typing import List, Tuple, Dict


def get_sentence_and_tags(
    tree: LexicalTree, tags: List[IGTag]
) -> Tuple[str, List[Tuple[str, int, int, str]]]:
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

    return (sentence, tags_tuples)


def write_mae_representation(
    output_file, trees_with_tags: List[Tuple[LexicalTree, List[IGTag]]]
):
    sentences_with_tags = [
        get_sentence_and_tags(tree, tags) for tree, tags in trees_with_tags
    ]

    with open(output_file, "w", encoding="utf-8") as output:
        output.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
        output.write("<ADICO_test_1>\n")

        text = "\n".join([sentence for sentence, _ in sentences_with_tags])
        output.write(f"<TEXT><![CDATA[{text}]]></TEXT>\n")

        output.write("<TAGS>\n")

        tag_ids: Dict[str, int] = defaultdict(int)
        tag_to_shorthand = {
            "aIm": "a",
            "Attribute": "A",
            "oBject": "o",
            "aCtor": "aC",
            "SEPARATOR": "S",
            "Deontic": "D",
        }
        offset = 0
        id = 0
        for sentence, tags in sentences_with_tags:
            for tag_name, start, stop, tag_text in tags:
                spans = f"{offset + start}~{offset + stop}"
                tag_repr = f'<{tag_name} id="{tag_to_shorthand[tag_name]}{tag_ids[tag_name]}" spans="{spans}" text="{sentence[start:stop]}" />\n'
                output.write(tag_repr)
                tag_ids[tag_name] += 1
            offset += len(sentence) + 1

        output.write("</TAGS>\n")

        output.write("</ADICO_test_1>")
