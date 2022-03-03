"Functions to enumerate splittings of an integer (supporting various constraints)"
# MCS 275 Spring 2022 Project 2 Solution
# David Dumas

# See below for another method to implement `splittings`
def splittings(n):
    "Recursively find all splittings of n"
    if n <= 0:
        raise ValueError()
    if n == 1:
        return [ [1] ]
    else:
        L = splittings(n-1)
        # There are two ways to "promote" a splitting of n-1 to a splitting of n
        #  1) Add one at the end   2) Add one to the last item
        # This sum of list comprehensions applies both to each element of L
        return [ x + [1] for x in L ] + [ x[:-1] + [x[-1]+1] for x in L ]

# See below for several other methods to implement `splittings_iterative`
def splittings_iterative(n):
    "Iteratively find all splittings of n"
    # This is a direct translation of `splittings` to iteration
    if n <= 0:
        raise ValueError()
    L = [ [1] ] # a splitting of 1
    # Each iteration of this loop promotes splittings to have sum
    # one larger than last time
    for _ in range(n-1):
        L = [ x + [1] for x in L ] + [ x[:-1] + [x[-1]+1] for x in L ]
    return L

splittings_cache = {}

def splittings_memoized(n):
    "Recursively find all splittings of n, with memoization"
    # This implements the method of `splittings()`
    if n <= 0:
        raise ValueError()
    if n in splittings_cache:
        return splittings_cache[n]
    L = [ [n] ]
    for k in range(1,n):
        for s in splittings_memoized(n-k):
            L.append( [k] + s )
    splittings_cache[n] = L
    return L

def splittings_into(n,parts):
    "Find splittings of n into given parts"
    if n <= 0:
        raise ValueError()
    L = []
    # Iterate over the available parts
    # for each, find splittings that start with that part
    for p in parts:
        if p==n:
            # If n is an available part, then [n] is a valid splitting
            L.append([p])
        elif p<n:
            # We can use p, but then there is still n-p left over.
            # This recursive call will generate splittings of n-p.
            for s in splittings_into(n-p,parts):
                L.append([p] + s)
    return L

def splittings_distinct(n):
    "Find splittings of n into distinct parts"
    if n <= 0:
        raise ValueError()
    # splittings_distinct is a special case of splittings_distinct_into
    # where the allowed parts are 1, 2, ..., n
    return splittings_distinct_into(n,list(range(1,n+1)))

def splittings_distinct_into(n,parts):
    "Find splittings of n into distinct parts from a list"
    if n <= 0:
        raise ValueError()
    L = []
    for i,p in enumerate(parts):
        # p is an allowed part
        # i is the index where it appears in parts
        if p==n:
            L.append([p])
        elif p<n:
            others = parts[:i] + parts[i+1:] # Like parts, but with p dropped
            for s in splittings_distinct_into(n-p,others):
                L.append([p] + s)
    return L

def splittings_limited_size(n,maxparts):
    "Find splittings of n up to a certain maximum size"
    if n <= 0:
        raise ValueError()
    if n==0:
        return []
    L = [ [n] ]
    if maxparts > 1:
        for k in range(1,n):
            # Recursive calls decreate maxparts so we automatically
            # give up if the splitting becomes too big.
            for s in splittings_limited_size(n-k,maxparts-1):
                L.append( [k] + s )
    return L



#----------------------------------------------------------------------
# ALTERNATE METHOD TO SOLVE `splittings()`
# Included for informational purposes only, not required reading!

def splittings2(n):
    "Recursively find all splittings of n, alternate method"
    if n <= 0:
        raise ValueError()
    L = [ [n] ] # The only 1-part splitting
    # Now find the multipart splittings
    for k in range(1,n):
        # We've decided to use `k` as a part
        # The rest of the splitting is thus a splitting of `n-k`
        for s in splittings2(n-k):
            L.append( [k] + s )
    return L

#----------------------------------------------------------------------

#----------------------------------------------------------------------
# SEVERAL OTHER METHODS TO SOLVE `splittings_iterative()`
# Included for informational purposes only, not required reading!

def splittings_iterative2(n):
    "Iteratively find all splittings of n, alternate method"
    # This is a direct translation of `splittings2` to iteration
    if n <= 0:
        raise ValueError()
    finished = [] # finished splittings
    partials = [ [] ] # splittings still missing some parts
    # We'll repeatedly pull out a partial splitting, find all ways to add
    # one more part to it, and add those to `partial` or `finished` as
    # appropriate.
    while partials:
        x = partials.pop()
        s = sum(x)  # could cache the sum for slight speed improvement
        if s == n:
            finished.append(x)
        else:
            for i in range(1,n-s+1):
                partials.append(x+[i])
    return finished

def splittings_iterative3(n):
    "Iteratively find all splittings of n, another alternate method"
    # There are 2**(n-1) splittings, which can be seen as follows.
    # Imagine a string of n beads:
    #  @-@-@-@-@-@  (n=6 here)
    # There are n-1 gaps between beads where you can cut the string.
    # If you make some cuts, the result is a splitting:
    #  @ @-@-@ @-@  -> [1,3,2], a splitting of 6
    # If we have a (n-1)-bit binary number, we can think of the bits
    # as instructions, where 0 means "don't cut" and 1 means "cut".
    # E.g. if the number is 0b011001b = 25, then the bits line up as
    #  @-@-@-@-@-@
    #   0 1 1 0 1
    # which means cutting like this
    #  @-@ @ @-@ @
    # corresponding to splitting [2,1,2,1].
    #
    # This function finds all splittings using this method, iterating
    # through all 2**(n-1) integers represented by (n-1) bits.
    if n <= 0:
        raise ValueError()
    L=[]
    for k in range(2**(n-1)):
        # We'll find the binary digits of k
        # As we go, we'll keep track of how many "beads" have passed
        # since the last cut, in a variable `i`
        s = [] # splitting we're developing
        i = 1  # number of beads since the last cut
        for _ in range(n-1):
            if k%2:
                # bit 1 means cut and record size
                s.append(i)
                i=0
            i+=1
            k=k>>1 # move to next bit
        # We've reached the end of the string, so `i` becomes
        # the final part of this splitting
        s.append(i)
        # Add it to the list of splittings
        L.append(s)
    return L

def splittings_iterative4(n):
    "Iteratively find all splittings of n with an incomprehensible one-line function"
    # The next line actually does the same thing as splittings_iterative3, but is slower.
    # It doesn't raise ValueError for negative n, but could do so at the cost of two more lines.
    return [ [len(p) for p in ("@"+"".join(a+b for a,b in zip(("{:0"+str(n-1)+"b}").format(k),"@"*(n-1)))).replace("0","").split("1")] for k in range(2**(n-1))]

#----------------------------------------------------------------------
