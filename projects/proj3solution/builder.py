# MCS 275 Spring 2022 Project 3 Solution
# Emily Dumas
import plane
import pointtree
import sys

def TST_from_file(fn):
    """
    Read file named `fn` (text with one point on each line as 'x y')
    Return a TST of the points read from that file.
    """
    T = pointtree.TST()
    with open(fn,"r",encoding="UTF-8") as fp:
        for line in fp:
            x,y = [int(x) for x in line.split()]
            p = plane.Point2(x,y)
            T.insert(p)
    return T


if __name__=="__main__":
    # We're run as a script, so take first command line argument as
    # the input filename
    if len(sys.argv) < 2:
        print("USAGE: {} INPUTFILE".format(sys.argv[0]))
        exit(1)

    T = TST_from_file(sys.argv[1])

    print("Built a TST with:")
    print("Root = ({},{})".format(T.key.x,T.key.y))
    print("Number of nodes = {}".format(len(T)))
    print("Depth = {}".format(T.depth()))
    print("Fill fraction = {}%".format(int(100*T.fill_fraction())))
