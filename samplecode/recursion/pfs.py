"Paper folding sequence"
# MCS 275 Spring 2022 Lecture 12

# pfs(1)
# 1

# pfs(2)
#  1       1   0
#  pfs(1)  1   flip(pfs(1)^r)

# pfs(3)
# 110 1 100

# pfs(4)
# 110110011100100

# pfs(5)
# ...

def pfs(n):
    """
    Return the paper folding sequence for
    n folds.
    """
    if n < 0:
        raise ValueError("PFS only defined for n>=0")
    if n == 0:
        return []
    if n == 1:
        return [1]
    prev = pfs(n-1)
    return prev + [1] + [1-x for x in prev[::-1]]
    

def pfs_iterative(n):
    """
    Return the paper folding sequence for
    n folds (using iteration).
    """
    if n < 0:
        raise ValueError("PFS only defined for n>=0")
    L = [] # unfolded piece of paper
    for _ in range(n):
        # fold the paper
        L = L + [1] + [1-x for x in L[::-1]]
    return L
