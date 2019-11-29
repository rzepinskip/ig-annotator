from os import listdir
from os.path import isfile, join
import pandas as pd
from column import Column
from root import Root


def check_tag(row, tag):
    return row[Column.TAG] == tag


def check_relation(row, rel):
    return row[Column.RELATION] == rel


def is_aim_for_deontic(row):
    return check_tag(row, 'VERB') and check_relation(row, 'xcomp')


def is_attribute(row):
    return check_tag(row, 'NOUN') and check_relation(row, 'nsubj')


def is_actor(row):
    return check_tag(row, 'NOUN') and check_relation(row, 'obj')


def get_aim_and_deontic(df, root):
    if not check_tag(root, 'VERB'):
        return False

    result = Root(root)

    children = df.loc[df[Column.PARENT] == root[Column.ID]]
    rest = df.loc[df[Column.PARENT] != root[Column.ID]]
    for index, child in children.iterrows():
        if is_aim_for_deontic(child):
            result.append("aim", child)
        elif is_attribute(child):
            result.append("attribute", child)
        elif is_actor(child):
            result.append("actor", child)
        else:
            result.append("undefined", child)

    if not result.switch_aim_if_no_deontic():
        rest = result.append_children(rest, "aim")

    rest = result.append_children(rest, "attribute")

    rest = result.append_children(rest, "actor")

    result.append_children(rest, "undefined")

    return result


def annotate_file(file_path):
    with open(file_path, 'r+') as f:
        df = pd.read_csv(f, sep="\t", header=None)
    roots = df.loc[df[Column.RELATION] == 'root']
    rest = df.loc[df[Column.RELATION] != 'root']
    result = []
    for index, row in roots.iterrows():
        result.append(get_aim_and_deontic(rest, row))
    print(result)


directory = "conllu/goldStandard-stanford"
for f in listdir(directory):
    file_path = join(directory, f)
    if isfile(file_path):
        try:
            annotate_file(file_path)
        except Exception as e:
            print(str(e) + " in " + f)
