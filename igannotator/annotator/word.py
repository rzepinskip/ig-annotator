import pandas as pd

class Word:
    def __init__(self, row):
        self.id = row[0]
        self.value = row[1]
        self.lemm = row[2]
        self.tag = row[3]
        self.parent = row[6]
        self.relation = row[7]
        self.children = []
        self.ig_tag = None

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
        return f"{self.value} ({self.ig_tag}):\n\t" + "\n\t".join([f"{x.tag}, {x.relation}, {x.ig_tag} :{x.get_all_descendants()}" for x in self.children])

    def to_connlu(self):
        return ""

def annotate_df(df):

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

    return root