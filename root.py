from group import Group


class Root:
    def __init__(self, root):
        self.groups = {
            "attribute": [],
            "deontic": [Group(root)],
            "aim": [],
            "actor": [],
            "undefined": []
        }

    def __repr__(self):
        return str(self)

    def __str__(self):
        result = ""
        for key in self.groups:
            if len(self.groups[key]) == 1:
                result += self.str_object(key)
            elif len(self.groups[key]) > 1:
                result += self.str_array(key)

        return result

    def str_object(self, key):
        return key + ": " + str(self.groups[key][0]) + "\n"

    def str_array(self, key):
        return key + ":[" + " | ".join([str(item) for item in self.groups[key]]) + "]\n"

    def append(self, key, item):
        self.groups[key].append(Group(item))

    def switch_aim_if_no_deontic(self):
        if len(self.groups["aim"]) == 0:
            self.groups["aim"] = self.groups["deontic"]
            self.groups["deontic"] = []
            return True
        return False

    def append_children(self, rest, key):
        for i in range(len(self.groups[key])):
            self.groups[key][i].children = Group.append_children(rest, self.groups[key][i])
            rest = self.groups[key][i].remove_children_for_df(rest)
        return rest
