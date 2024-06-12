# MCS 275 Spring 2022 Project 3 Solution
# Emily Dumas
"Trisection search trees for points in the plane"

class TST:
    "Trisection search tree node"
    def __init__(self,key=None):
        """
        Initialize a new empty TST node, or if `key` is given (a plane.Point2
        object), make a new node with that key.
        """
        self.key = key
        self.child = [None,None,None]
        self.parent = None

    def get_child(self,i):
        "Return the node that is child `i` of this one"
        return self.child[i]

    def set_child(self,i,node):
        "Set `node` to be child `i` of this one"
        self.child[i] = node
        if node != None:
            node.parent = self

    def __str__(self):
        """
        Human-readable string representation showing key and which children
        are present.
        """
        # Assemble the 3-character string describing children
        child_desc = "" 
        for c in self.child:
            if c == None:
                child_desc += "."
            else:
                child_desc += "@"
        # Make a string describing the key
        if self.key:
            key_desc = "({},{})".format(self.key.x,self.key.y)
        else:
            key_desc = "None"

        return "TST(key={},children=[{}])".format(key_desc,child_desc)

    def __repr__(self):
        "Unambiguous string representation"
        # We choose to just use the same string as __str__
        return str(self)

    def insert(self,p):
        "Add a new node somewhere in this TST with key `p`"
        if self.key==None:
            # Empty TST, add it here
            self.key = p
            return
        # Not empty; need to know relative position to current key
        i = self.key.sector_of(p)
        if self.child[i] == None:
            # Available spot for a child, so add it as a child of this node
            self.set_child(i,TST(p))
        else:
            # There's already a child at that spot, so ask them to handle
            # the .insert()
            self.child[i].insert(p)

    def search(self,p):
        "Return a node from this TST with key `p`, or `None` if no such node exists"
        if self.key == None:
            # The empty tree definitely doesn't contain a node with key `p`
            return None
        if self.key == p:
            # This node is the one! Return it.
            return self
        # This is not the node, so we need to know where to descend
        # to continue the search
        i = self.key.sector_of(p)
        if self.child[i] == None:
            # There's no child in the only part of the tree that could
            # contain `p`, so we know `p` isn't present at all.
            return None
        else:
            # Delegate the search to the node that is the root of the
            # subtree that may contain `p`
            return self.child[i].search(p)

    def __contains__(self,p):
        "Returns True if this TST contains a node with key `p`"
        return self.search(p) != None
        # Equivalent alternative: return bool(self.search(p))

    def __len__(self):
        "Number of nodes in this TST"
        if self.key==None:
            return 0
        n = 1 # counts this node
        for c in self.child:
            if c == None:
                continue # ignore missing children
            n += len(c) # counts the nodes in each child subtree
                        # len(c) becomes c.__len__()
        return n

    def depth(self):
        "Maximum length (in edges) of a descending path in this TST"
        d = 0
        for c in self.child:
            if c == None:
                continue # ignore missing children
            d = max(d, 1+c.depth()) # A path going to child `c` has length 1 + (longest path in that subtree)
                                    # so consider that as a contender, taking max() to ignore it in case
                                    # one of the other children already gave a larger depth.
        return d
    
    def max_nodes_for_depth(self,d):
        "The maximum number of nodes that a TST of depth `d` can contain"
        # Each new level of the tree can have 3 times as many nodes as the one
        # above it, so a full tree has levels whose sizes are 1, 3, 9, ...
        #
        # Recall the geometric series summation formula
        #   1 + r + r**2 + r**3 + ... + r**d = (r**(d+1) - 1) / 2
        # So in this case we have
        #   1 + 3 + 9 + ... + 3**(d) = (3**(d+1) - 1) / 2
        #
        # It would also be OK to just make a loop that adds 1, 3, 9, ...
        # but the direct formula is faster.
        return (3**(d+1) - 1) // 2

    def fill_fraction(self):
        """
        Return the ratio of the number of nodes in this TST to the maximum
        number a TST of this depth could contain.
        """
        return len(self) / self.max_nodes_for_depth(self.depth())

