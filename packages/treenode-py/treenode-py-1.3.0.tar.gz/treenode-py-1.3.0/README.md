# [TreeNode](https://pypi.org/project/treenode-py/)

TreeNode is a Python library that provides functionality to create and manipulate tree structures.

------

## Installation
You can install TreeNode using pip:
```
pip install treenode-py
```

## Usage
To use TreeNode, start by importing the TreeNode class from the treenode module:
```python
from treenode import TreeNode
```
### Tree
You can create a tree by initializing a TreeNode object with the root node's name:
```python
tree = TreeNode("name of the root node")
```

### Child Nodes
To add child nodes to the tree, use the `add_child()` method:
```python
child1 = tree.add_child("name of child node 1")
```
You can use the `slash=False` to remove a slash after node:
```python
child2 = tree.add_child("name of child node 2", slash=False)
```

You can also add subchild nodes to existing child nodes:
```python
subchild1 = child1.add_child("Subchild 1", slash=False)
subchild2 = child1.add_child("Subchild 2", slash=False)
```

### Printing the Tree and Nodes
To print the tree, simply use the `print()` function:
```python
print(tree)
```
This will be our full code:
```python
from treenode import TreeNode

tree = TreeNode("name of tree")
child1 = tree.add_child("name of child node 1")
child2 = tree.add_child("name of child node 2", slash=False)
subchild1 = child1.add_child("Subchild 1", slash=False)
subchild2 = child1.add_child("Subchild 2", slash=False)
print(tree)
```

This will output(check github if you on pypi):
```
Root/
├── Child 1/
│   ├── Subchild 1
│   └── Subchild 2
└── Child 2
```

You can retrieve various information about the tree, such as the depth, number of files, number of folders, list of files, and list of folders.

## Documentation

### Class Methods

#### `__init__(self, name, slash=True)`

Initializes a tree node.

- `name (str)`: The name of the node.
- `slash (bool, optional)`: Indicates whether the node represents a directory path with `/`. Defaults to `True`.

Usage:
```python
from treenode import TreeNode

tree1 = TreeNode("name of empty tree with directory slash")
tree2 = TreeNode("name of empty tree without directory slash", slash=False)
print(tree1)
print(tree2)
```

#### `add_child(self, name, slash=True)`

Creates a child node with the given name and adds it to the current node.

- `name (str)`: The name of the child node.
- `slash (bool, optional)`: Indicates whether the node represents a directory path with `/`. Defaults to `True`.

Usage:
```python
from treenode import TreeNode

tree = TreeNode("name of tree")
folderchild = tree.add_child("name of child node 1")
filechild = tree.add_child("name of child file", slash=False)
filechild_of_folderchild = folderchild.add_child("name of subchild file", slash=False)
print(tree)
```

#### `generate_treepath(self, path)`

Generates a tree structure for the given directory path.

- `path (str)`: The directory path.

Returns:
- `TreeNode`: The root node of the generated tree structure.

Usage:
```python
from treenode import TreeNode
import os

path = input("Enter the path to the folder: ")
tree = TreeNode(os.path.basename(path)).generate_treepath(path)
print(tree)
```

#### `find_node(self, name)`

Finds a node with the given name.

- `name (str)`: The name of the node to find.

Returns:
- `TreeNode or None`: The node if found, otherwise `None`.

Usage:
```python
from treenode import TreeNode

tree = TreeNode("name of tree")
folder = tree.add_child("name of folder")
file = folder.add_child("name of file", slash=False)
node_name = "name of folder"
found_node = tree.find_node(node_name)
print(tree)
print(f"Node '{node_name}' found: \n{found_node}")
```

#### `is_empty(self)`

Checks if the node is empty (has no children).

Returns:
- `bool`: `True` if the node is empty, otherwise `False`.

Usage:
```python
from treenode import TreeNode

tree = TreeNode("name of tree")
empty = tree.is_empty()
print(tree)
print(f"Tree is empty?: {empty}")
```

#### `get_depth(self)`

Calculates the depth of the tree.

Returns:
- `int`: The depth of the tree.

Usage:
```python
from treenode import TreeNode

tree = TreeNode("name of tree")
folder = tree.add_child("name of folder")
file = folder.add_child("name of file", slash=False)
depth = tree.get_depth()
print(tree)
print(f"Depth: {depth}")
```

#### `get_files(self)`

Retrieves a list of all files in the tree.

Returns:
- `list`: A list of file names.

Usage:
```python
from treenode import TreeNode

tree = TreeNode("name of tree")
file = tree.add_child("name of file", slash=False)
getted = tree.get_folders()
print(tree)
print(f"Files: {getted}")
``` 

#### `get_folders(self)`

Retrieves a list of all folders in the tree.

Returns:
- `list`: A list of folder names.

Usage:
```python
from treenode import TreeNode

tree = TreeNode("name of tree")
folder = tree.add_child("name of folder")
getted = tree.get_folders()
print(tree)
print(f"Folders: {getted}")
``` 

#### `count_files(self)`

Counts the total number of files in the tree.

Returns:
- `int`: The total number of files.

Usage:
```python
from treenode import TreeNode

tree = TreeNode("name of tree")
file = tree.add_child("name of file", slash=False)
counted = tree.count_files()
print(tree)
print(f"Files: {counted}")
``` 

#### `count_folders(self)`

Counts the total number of folders in the tree.

Returns:
- `int`: The total number of folders.

Usage:
```python
from treenode import TreeNode

tree = TreeNode("name of tree")
folder = tree.add_child("name of folder")
counted = tree.count_folders()
print(tree)
print(f"Folders: {counted}")
``` 
