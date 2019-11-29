from column import Column


class Group:
    def __init__(self, row, children=None):
        self.value = row[Column.VALUE]
        self.id = row[Column.ID]
        self.children = [] if children is None else children

    def __repr__(self):
        return str(self)

    def __str__(self):
        children = ""
        if len(self.children) > 0:
            children += " [" + " ".join([str(child) for child in sorted(self.children, key=lambda x: int(x.id))]) + "]"
        return self.value + children

    @classmethod
    def append_children(cls, df, parent):
        result = []
        for index, child in df.iterrows():
            if child[Column.PARENT] == parent.id:
                group_child = Group(child)
                result.append(group_child)
                result += cls.append_children(df, group_child)

        return result

    def remove_children_for_df(self, df):
        children = [item.id for item in self.children]
        return df[~df[Column.ID].isin(children)]
