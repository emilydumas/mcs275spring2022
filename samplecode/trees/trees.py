class Node:
    "Node in a binary tree"
    def __init__(self,key=None,left=None,right=None,parent=None):
        """Create a new node with left child `left`,
        right child `right`, and key `key`"""
        self.left = left
        self.right = right
        self.parent = parent
        self.key = key
    def __str__(self):
        "Human-readable string representation"
        return '[{}]'.format(self.key)
    def __repr__(self):
        "Unambiguous string representation"
        return str(self)
    def set_left(self,other):
        "Make node `other` the left child of this one"
        self.left = other
        other.parent = self
    def set_right(self,other):
        "Make node `other` the right child of this one"
        self.right = other
        other.parent = self
    
class BST(Node):
    "Binary search tree class (with recursive insert, search)"
    def search(self,k):
        """
        Find a node in this tree with key `k` and return it;
        return None if no such node exists.
        """
        if k == self.key:
            return self
        elif k < self.key:
            # the node with key `k` must be in the left subtree
            if self.left == None:
                return None
            else:
                return self.left.search(k)
        elif self.key < k:
            # the node with key `k` must be in the right subtree
            if self.right == None:
                return None
            else:
                return self.right.search(k)

    def insert(self,k):
        """
        Find a suitable place to add a new node to this BST
        with key `k`, and add it.
        """
        if k <= self.key:
            if self.left == None:
                # k belongs to the left, and the left is empty.
                self.set_left(BST(key=k))
            else:
                # Have the left subtree handle it!
                self.left.insert(k)
        else:
            if self.right == None:
                self.set_right(BST(key=k))
            else:
                self.right.insert(k)


