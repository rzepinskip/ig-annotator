import pandas as pd

class LexicalTree:
    def __init__(self, row):
        self.id = row[0]
        self.value = row[1]
        self.lemm = row[2]
        self.tag = row[3]
        self.polarity = row[5]
        self.parent = row[6]
        self.relation = row[7]
        self.children = []

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.value

    def flatten(self):
        children = [x.flatten() for x in self.children]
        children_str = str(children) if len(children) > 0 else ""
        return self.value + children_str

    def get_all_descendants(self):
        descendants = [self] + [y for x in self.children for y in x.get_all_descendants()]
        descendants.sort(key=lambda x: x.id)
        return descendants

    def show_children_subtrees(self):
        return f"{self.value}:\n\t" + "\n\t".join([f"{x.tag}, {x.relation}:{x.get_all_descendants()}" for x in self.children])

    def to_connlu(self):
        return ""

def annotate_df(df):

    id_to_word = dict()
    for index, row in df.iterrows():
        node = LexicalTree(row)
        id_to_word[node.id] = node

    root = None
    for node in id_to_word.values():
        if node.parent == 0:
            root = node
            continue
        id_to_word[node.parent].children.append(node)

    return root