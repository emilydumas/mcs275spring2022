"Binary trees and binary search trees"
# MCS 275 Spring 2022 Lectures 18-21


class Node:
    "Node in a binary tree"

    def __init__(self, key=None, left=None, right=None, parent=None):
        """Create a new node with left child `left`,
        right child `right`, and key `key`"""
        self.left = left
        self.right = right
        self.parent = parent
        self.key = key

    def preorder(self):
        "Return a list of keys in preorder"
        L = []
        L.append(self.key)
        if self.left:
            L.extend(self.left.preorder())
        if self.right:
            L.extend(self.right.preorder())
        return L

    def postorder(self):
        "Return a list of node keys in preorder"
        L = []
        if self.left:
            L.extend(self.left.postorder())
        if self.right:
            L.extend(self.right.postorder())
        L.append(self.key)
        return L

    def inorder(self):
        "Return a list of node keys in preorder"
        L = []
        if self.left:
            L.extend(self.left.inorder())
        L.append(self.key)
        if self.right:
            L.extend(self.right.inorder())
        return L

    def __str__(self):
        "Human-readable string representation"
        return "[{}]".format(self.key)

    def __repr__(self):
        "Unambiguous string representation"
        return str(self)

    def set_left(self, other):
        "Make node `other` the left child of this one"
        self.left = other
        other.parent = self

    def set_right(self, other):
        "Make node `other` the right child of this one"
        self.right = other
        other.parent = self


class BST(Node):
    "Binary search tree class (with recursive insert, search)"

    def search(self, k):
        """
        Find a node in this tree with key `k` and return it;
        return None if no such node exists.
        """
        if self.key == None:
            return None
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

    def __contains__(self, k):
        """
        Return boolean indicating whether the tree contains
        a node with key k
        """
        return self.search(k) != None

    def insert(self, k):
        """
        Find a suitable place to add a new node to this BST
        with key `k`, and add it.
        """
        if self.key == None:
            # Empty tree, so just add k as the key of *this* node
            self.key = k
            return
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


# x in L
#  becomes
# L.__contains__(x)
