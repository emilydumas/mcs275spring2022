def solvemaze(M,path=None):
    """
    Find a solution to maze `M`
    using a depth-first recursive
    search.
    """
    print("Called with path={}".format(path))
    if path==None:
        # no path specified, so start
        # at M.start
        path = [M.start]
    if path[-1]==M.goal:
        # We've found a solution
        print("SOLVED!")
        return path
    # next steps to consider
    # (may include retracing our steps)
    steps = M.free_neighbors(*path[-1])
    for s in steps:
        if len(path)>=2 and s == path[-2]:
            print("Not considering {}, as it would retrace our steps".format(s))
            continue
        # Consider whether next step `s` leads to a solution
        print("Considering next step {}".format(s))
        soln = solvemaze(M,path + [s])
        if soln != None:
            # Some recursive call yielded a solution!
            print("Hooray, considering {} worked!".format(s))
            return soln
        # if we reach this line, step `s` only led to dead ends
    # if we reach this line, then no continuation of `path`
    # leads to a solution, only dead ends.
    print("Path {} leads only to dead ends".format(path))
    return None
