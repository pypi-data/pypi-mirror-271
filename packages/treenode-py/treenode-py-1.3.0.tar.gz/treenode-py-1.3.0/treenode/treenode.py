import os

class TreeNode:
    def __init__(self, name, slash=True):
        """
        Initializes a tree node.

        Args:
            name (str): The name of the node.
            slash (bool, optional): Indicates whether the node represents a directory path with /. Defaults to True.
        """
        self.name = name
        self.slash = slash
        self.children = []

    def add_child(self, name, slash=True):
        """
        Adds a child node to the current node.

        Args:
            name (str): The name of the child node.
            slash (bool, optional): Indicates whether the node represents a directory path with /. Defaults to True.
        """
        child_node = TreeNode(name, slash)
        self.children.append(child_node)
        return child_node

    def __repr__(self, level=0, last=False):
        """
        Returns a string representation of the tree.

        Args:
            level (int, optional): The level of the node in the tree. Defaults to 0.
            last (bool, optional): Indicates whether the node is the last child of its parent. Defaults to False.

        Returns:
            str: A string representation of the tree.
        """
        ret = ""
        if level > 0:
            ret += "│   " * (level - 1)
            ret += "├── " if not last else "└── "
        ret += self.name
        if self.slash:
            ret += "/"
        ret += "\n"
        for i, child in enumerate(self.children):
            last = i == len(self.children) - 1
            ret += child.__repr__(level + 1, last)
        return ret
    
    def generate_treepath(self, path):
        """
        Generates a tree representing the directory structure.

        Args:
            path (str): The root path of the directory structure.

        Returns:
            TreeNode: The root of the generated tree.
        """
        if os.path.isdir(path):
            for item in os.listdir(path):
                full_item_path = os.path.join(path, item)
                if os.path.isdir(full_item_path):
                    child_node = self.add_child(item)
                    child_node.generate_treepath(full_item_path)
                else:
                    self.add_child(item, slash=False)
        return self

    def find_node(self, name):
        """
        Finds a node with the given name.

        Args:
            name (str): The name of the node to find.

        Returns:
            TreeNode or None: The node if found, otherwise None.
        """
        if self.name == name:
            return self
        for child in self.children:
            found = child.find_node(name)
            if found:
                return found
        return None

    def is_empty(self):
        """
        Checks if the node is empty (has no children).

        Returns:
            bool: True if the node is empty, otherwise False.
        """
        return not self.children

    def get_depth(self):
        """
        Calculates the depth of the tree.

        Returns:
            int: The depth of the tree.
        """
        if not self.children:
            return 1
        return 1 + max(child.get_depth() for child in self.children)

    def get_files(self):
        """
        Retrieves a list of all files in the tree.

        Returns:
            list: A list of file names.
        """
        files = []
        if not self.slash:
            files.append(self.name)
        for child in self.children:
            files.extend(child.get_files())
        return files

    def get_folders(self):
        """
        Retrieves a list of all folders in the tree.

        Returns:
            list: A list of folder names.
        """
        folders = []
        if self.slash:
            folders.append(self.name)
        for child in self.children:
            folders.extend(child.get_folders())
        return folders

    def count_files(self):
        """
        Counts the total number of files in the tree.

        Returns:
            int: The total number of files.
        """
        count = 0
        if not self.slash:
            return 1
        for child in self.children:
            count += child.count_files()
        return count

    def count_folders(self):
        """
        Counts the total number of folders in the tree.

        Returns:
            int: The total number of folders.
        """
        count = 1 if self.slash else 0
        for child in self.children:
            count += child.count_folders()
        return count


if __name__ == "__main__":
    path = input("Enter the path to the folder: ")
    tree = TreeNode(os.path.basename(path)).generate_treepath(path)
    print(tree)

    node_name = input("Enter the name of the node to search for: ")
    found_node = tree.find_node(node_name)
    if found_node:
        print(f"Node '{node_name}' found: {found_node}")
    else:
        print(f"Node '{node_name}' was not found.")
