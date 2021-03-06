import click
import warnings
import pathlib

from igannotator.output.mae import write_mae_representation
from igannotator.annotator import IgAnnotator

@click.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path(exists=False))
def annotate_file(input, output):
    with open(input, "r") as f:
        input_text = f.read()

    annotator = IgAnnotator()
    sentences = [x for x in input_text.split("\n\n") if len(x) > 0]

    mae_data = list()
    for sentence in sentences:
        tree, tags = annotator.annotate(sentence)

        mae_data.append((tree, tags))

    write_mae_representation(output, mae_data)


if __name__ == "__main__":
    annotate_file()

