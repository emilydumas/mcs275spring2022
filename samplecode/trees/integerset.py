"Set of integers implemented in various ways"
# MCS 275 Spring 2022

import trees


class IntegerSetUL:
    """Unsorted list implementation of integer set"""

    def __init__(self, iterable=None):
        self.data = []
        if iterable:
            for x in iterable:
                self.add(x)

    def add(self, x):
        if not isinstance(x, int):
            raise ValueError("Only integers supported")
        self.data.append(x)

    def __contains__(self, x):
        return x in self.data

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return "{}({} items)".format(self.__class__.__name__, len(self.data))

    def __repr__(self):
        return str(self)


class IntegerSetSL:
    """Sorted list implementation of integer set"""

    def __init__(self, iterable=None):
        self.data = []
        if iterable:
            for x in iterable:
                self.add(x)

    def add(self, x):
        if x in self.data:
            return
        if not isinstance(x, int):
            raise ValueError("Only integers supported")
        self.data.append(x)
        self.data.sort()

    def __contains__(self, x):
        # Bisection search; look at middle value, decide whether
        # the desired element would appear earlier or later
        if not self.data:
            return
        low = 0
        high = len(self.data) - 1
        while low < high:
            mid = (low + high) // 2
            y = self.data[mid]
            if x == y:
                return True
            elif x < y:
                high = mid - 1
            else:
                low = mid + 1
        return x == self.data[low]

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return "{}({} items)".format(self.__class__.__name__, len(self.data))

    def __repr__(self):
        return str(self)


class IntegerSet:
    "Binary search tree integer set implementation"

    def __init__(self, iterable=None):
        self.tree = trees.BST()
        if iterable:
            for x in iterable:
                self.add(x)

    def add(self, x):
        if not isinstance(x, int):
            raise ValueError("Only integers supported")
        self.tree.insert(x)

    def __contains__(self, x):
        return x in self.tree

    def __str__(self):
        return "{}({} items)".format(self.__class__.__name__, len(self.data))

    def __repr__(self):
        return str(self)


if __name__ == "__main__":
    import random
    import time

    n = 20000
    Linsert = [random.randint(1, 5 * n) for _ in range(n)]
    Lcheck = [random.randint(1, 5 * n) for _ in range(n // 2)] + Linsert[: n // 2]
    random.shuffle(Lcheck)

    implementations = [IntegerSetUL, IntegerSetSL, IntegerSet]

    for cls in implementations:
        print("Testing {} with {} elements:".format(cls.__name__, n))
        t0 = time.time()
        S = cls(Linsert)
        t1 = time.time()
        checks = [x in S for x in Lcheck]
        t2 = time.time()
        print("{:.2f}s insert".format(t1 - t0))
        print("{:.2f}s membership test".format(t2 - t1))
