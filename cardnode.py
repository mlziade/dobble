import math

class CardNode:
    
    def __init__(self, value: int):
        self.children: list['CardNode'] = list()
        self.value: int = value
        self.level: int = None
        self.is_leaf: bool = False
    
    def update_level(self, level: int):
        self.level = level
    
    def add_card(self, child):
        self.children.append(child)
        self.is_leaf = False

    def print_card(self):
        print('Card: ' + str(self.value))

    def get_paths_to_leaves(self):
        paths = []
        self._dfs(self, [], paths)
        return paths
    
    def _dfs(self, node, path, paths):
        if node is None:
            return
        path.append(node.value)
        if not node.children:
            paths.append(list(path))
        else:
            for child in node.children:
                self._dfs(child, path, paths)
        path.pop()