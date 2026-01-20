import argparse
import ast
import os

from utils import get_value_from_odoorc


MANIFEST_FILE_NAME = "__manifest__.py"

ARGS = {
    ("module_name", ): {
        "help": "odoo module name",
    },
    ("--addons-path",): {
        "default": None,
        "help": "If not specified, uses the one in ~/.odoorc"
    },
}


class Node:
    def __init__(self, name):
        self.name = name
        self.parents = []
        self.children = []

    def set_parent(self, parent_node):
        if self not in parent_node.children:
            parent_node.children.append(self)
        if parent_node not in self.parents:
            self.parents.append(parent_node)

    def print_children(self, level=0):
        print('- ' * level + self.name)
        for child in self.children:
            child.print_children(level=level + 1)


class Tree:
    def __init__(self):
        self.nodes = []

    def add_node(self, name, parent_names):
        node = self.get_node(name)
        for parent_name in parent_names:
            parent_node = self.get_node(parent_name)
            node.set_parent(parent_node)

    def get_node(self, name):
        if node := next((node for node in self.nodes if node.name == name), None):
            return node
        node = Node(name)
        self.nodes.append(node)
        return node



def build_module_tree(addons_path=None):
    tree = Tree()
    addons_path = addons_path or get_value_from_odoorc("addons_path")
    for path in addons_path.split(','):
        for root, _dirs, files in os.walk(path):
            if MANIFEST_FILE_NAME not in files:
                continue

            manifest_path = os.path.join(root, MANIFEST_FILE_NAME)
            with open(manifest_path, 'r', encoding='utf-8') as manifest_file:
                manifest_content = manifest_file.read()
                manifest_data = ast.literal_eval(manifest_content)
                parent_names = manifest_data.get('depends', [])
                module_name = os.path.basename(root)
                tree.add_node(module_name, parent_names)

    return tree

def show_children_modules(module_name, addons_path=None):
    tree = build_module_tree(addons_path=addons_path)
    module_node = tree.get_node(module_name)
    module_node.print_children()


def main():
    parser = argparse.ArgumentParser()
    for key, value in ARGS.items():
        parser.add_argument(*key, **value)
    args = parser.parse_args()
    show_children_modules(args.module_name, addons_path=args.addons_path)

if __name__ == '__main__':
    main()
