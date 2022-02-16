# MCS 275 Spring 2022
"Recursive comparison sorts"

def merge(L0,L1):
    """
    Take sorted lists `L0` and `L1` and return
    a sorted list that has the same items as `L0+L1`
    """
    n0 = len(L0)
    n1 = len(L1)
    i0 = 0  # current item in L0
    i1 = 0  # current item in L1
    L = []
    while i0<n0 and i1<n1:   # while L0 still has stuff AND L1 still has stuff
        if L0[i0] <= L1[i1]: # not(P and Q) = (not P) or (not Q)
            # take L0[i0]
            L.append(L0[i0])
            i0 += 1
        else:
            # take L1[i1]
            L.append(L1[i1])
            i1 += 1
    # One of the lists may still contain unused items
    # Copy over items still in L0 (maybe none)    
    while i0 < n0:
        L.append(L0[i0])
        i0 += 1
    # Copy over items still in L1 (maybe none)
    while i1 < n1:
        L.append(L1[i1])
        i1 += 1
    return L

def mergesort(L):
    "Return a list with the same items as L, but in sorted order"
    n = len(L)
    if n <= 1:
        return L
    else:
        L0=L[:n//2]  # roughly first half of L
        L1=L[n//2:]  # roughly second half of L
        return merge( mergesort(L0), mergesort(L1) )
