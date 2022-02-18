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


def partition(L,start=0,end=None):
    """
    Partition the part of L between indices start and end
    (not including end) in place, using last element of that 
    part of the list as a pivot.
    Returns the final position of pivot in the list.
    """
    if end == None:
        end = len(L)
    dst = start
    pivot = L[end-1]
    for src in range(start,end):
        if L[src]<pivot:
            # L[src] is small, put it at the next unused place
            # near the beginning of the list
            L[src],L[dst] = L[dst],L[src]
            dst += 1
    # Put the pivot in place
    L[end-1],L[dst] = L[dst],L[end-1]
    return dst

def quicksort(L,start=0,end=None):
    """
    Quicksort the part of list L between indices
    start and end in place.
    """
    if end == None:
        end = len(L)
    if end-start > 1:
        # there are at least two elements,
        # so some work is necessary
        print("Quicksort called on",L[start:end])
        m = partition(L,start,end)
        quicksort(L,start,m)
        quicksort(L,m+1,end)

if __name__=="__main__":
    import random
    print("\n\nTesting partition")
    L = [ random.randrange(20) for _ in range(15) ]
    p = L[-1]
    print(L)
    m = partition(L)
    print(L[:m],[L[m]],L[m+1:])
    assert L[m] == p
    assert all( [ x < p for x in L[:m] ])
    assert all( [ x >= p for x in L[m:] ])
    
    print("\n\nTesting quicksort")
    L = [ random.randrange(20) for _ in range(15) ]
    print("BEFORE:",L)
    quicksort(L)
    print(" AFTER:",L)
    assert L == sorted(L) # checks that Python thinks L is sorted