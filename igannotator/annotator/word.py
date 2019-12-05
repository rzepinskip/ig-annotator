class Word:
    def __init__(self, row):
        self.id = row[0]
        self.value = row[1]
        self.tag = row[3]
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
        return self.value + ":\n\t" + "\n\t".join([x.tag + ": " + str(x.get_all_descendants()) for x in self.children])

    def to_connlu(self):
        return ""
