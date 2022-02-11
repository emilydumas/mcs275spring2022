# MCS 275 Spring 2022 - David Dumas
"""Module for dealing with mazes represented as
rectangular arrays of cells, each of which can be
marked "free" or "blocked"."""

import random

class Maze:
    """Rectangular grid of free/blocked cells.
    Optionally, can store a starting point and goal."""
    neighbor_disps = [ (-1,0), (0,-1), (1,0), (0,1) ]
    def __init__(self, xsize, ysize, start=None, goal=None):
        """Initialize new empty maze"""
        self.xsize = xsize
        self.ysize = ysize
        self.start = start
        self.goal = goal
        self.grid = [ [" "]*self.xsize for _ in range(self.ysize) ]
    
    def __str__(self):
        """Crude text picture"""
        return "\n".join("".join(r) for r in self.grid)

    def __repr__(self):
        """Default to using str() for everything"""
        return str(self)

    def is_valid(self,x,y):
        """Is (x,y) a valid position for this maze?"""
        if x<0 or x>=self.xsize:
            return False
        if y<0 or y>=self.ysize:
            return False
        return True

    def insist_valid(self,x,y):
        """Raise exception if (x,y) not a valid position"""
        if not self.is_valid(x,y):
            raise ValueError("Position ({},{}) invalid for this maze with (xsize,ysize)=({},{})".format(
                x,
                y,
                self.xsize,
                self.ysize
            ))

    def is_free(self,x,y):
        """Is the cell at (x,y) free?"""
        self.insist_valid(x,y)        
        return self.grid[y][x] == " "

    def is_blocked(self,x,y):
        """Is the cell at (x,y) blocked?"""
        return not self.is_free(x,y)

    def set_free(self,x,y):
        """Make the cell at (x,y) free"""
        self.insist_valid(x,y)        
        self.grid[y][x] = " "

    def set_blocked(self,x,y):
        """Make the cell at (x,y) free"""
        self.insist_valid(x,y)
        self.grid[y][x] = "@"

    def free_neighbors(self,x,y):
        """Return list of neighbors of (x,y) that
        are currently free"""
        nbrs = []
        for dx,dy in self.neighbor_disps:
            try:
                if self.is_free(x+dx,y+dy):
                    nbrs.append((x+dx,y+dy))
            except ValueError:
                continue
        return nbrs

    def apply_border(self):
        """Make all edge cells blocked"""
        self.grid[0] = ["@"]*self.xsize
        self.grid[-1] = ["@"]*self.xsize
        for y in range(1,self.ysize-1):
            self.grid[y][0] = "@"
            self.grid[y][-1] = "@"

    def save_png(self,fn,scale=1,highlight=[]):
        """Save maze to a PNG file (requires PIL
        or Pillow module)"""
        m = scale
        import PIL.Image
        import PIL.ImageDraw
        img = PIL.Image.new("RGB",(m*self.xsize,m*self.ysize))
        draw = PIL.ImageDraw.Draw(img)
        for x in range(self.xsize):
            for y in range(self.ysize):
                fillcolor = (255,255,255)
                if self.is_blocked(x,y):
                    fillcolor = (50,50,50)
                elif self.start == (x,y):
                    fillcolor = (200,150,100)
                elif self.goal == (x,y):
                    fillcolor = (0,200,0)
                elif (x,y) in highlight:
                    fillcolor = (150,150,240)
                draw.rectangle([(x*m,y*m),((x+1)*m-1,(y+1)*m-1)],fill=fillcolor)
        img.save(fn,format="PNG")

    def save_svg(self,fn,highlight=[]):
        """Save maze to a PNG file (requires PIL
        or Pillow module)"""
        rmax = max(self.xsize,self.ysize)
        m = max(1,720//rmax)
        with open(fn,"wt") as outfile:
            outfile.write('<?xml version="1.0" standalone="no"?>\n')
            outfile.write('<svg width="{}" height="{}" version="1.1" xmlns="http://www.w3.org/2000/svg">\n'.format(m*self.xsize,m*self.ysize))
            outfile.write('<rect x="{}" y="{}" width="{}" height="{}" stroke="none" fill="white"/>\n'.format(0,0,m*self.xsize,m*self.ysize))
            for x in range(self.xsize):
                for y in range(self.ysize):
                    fillcolor = None
                    if self.is_blocked(x,y):
                        fillcolor = (50,50,50)
                    elif self.start == (x,y):
                        fillcolor = (200,150,100)
                    elif self.goal == (x,y):
                        fillcolor = (0,200,0)
                    elif (x,y) in highlight:
                        fillcolor = (150,150,240)
                    if fillcolor:
                        outfile.write('<rect x="{}" y="{}" width="{}" height="{}" stroke="none" fill="{}"/>\n'.format(
                            x*m,
                            y*m,
                            m,
                            m,
                            tohexcolor(fillcolor)
                        ))
            outfile.write('</svg>')

class PrimRandomMaze(Maze):
    """Randomly generated maze using Prim's algorithm:
    https://en.wikipedia.org/wiki/Prim%27s_algorithm
    (Known for producing mazes with lots of short dead
    ends, only moderately challenging for humans.)"""
    frontier_disps = [ (-2,0), (0,-2), (2,0), (0,2) ]
    def __init__(self,xsize,ysize):
        """Create a new random maze of size (xsize,ysize).
        Both dimensions must be odd."""
        super().__init__(xsize,ysize)
        if self.xsize%2==0 or self.ysize%2==0:
            raise ValueError("xsize and ysize must be odd")
        self.grid = [ ["@"]*self.xsize for _ in range(self.ysize) ]
        self.generate()
        self.start = (1,1)
        self.goal = (self.xsize-2,self.ysize-2)
        assert self.is_free(*self.start)
        assert self.is_free(*self.goal)

    def generate(self):
        """Make the maze using Prim's algorithm"""
        sx = 2*random.randrange(self.xsize//2)+1
        sy = 2*random.randrange(self.ysize//2)+1
        self.set_free(sx,sy)
        frontier = self.cell_frontier(sx,sy)
        while frontier:
            x,y = frontier.pop(random.randrange(len(frontier)))
            nbrs2 = self.cell_neighbors2(x,y)
            if nbrs2:
                x2,y2 = random.choice(nbrs2)
                x1 = (x+x2)//2
                y1 = (y+y2)//2
                self.set_free(x,y)
                self.set_free(x1,y1)
                nf = self.cell_frontier(x,y)
                for xf,yf in nf:
                    if (xf,yf) not in frontier:
                        frontier.append((xf,yf))

    def cell_frontier(self,x,y):
        """Return cells at +-2 in x or y that are blocked"""
        F = []
        for dx,dy in self.frontier_disps:
            x2,y2 = x+dx,y+dy
            if self.is_valid(x2,y2) and self.is_blocked(x2,y2):
                F.append((x2,y2))
        return F

    def cell_neighbors2(self,x,y):
        """Return cells at +-2 in x or y that are free"""
        F = []
        for dx,dy in self.frontier_disps:
            x2,y2 = x+dx,y+dy
            if self.is_valid(x2,y2) and self.is_free(x2,y2):
                F.append((x2,y2))
        return F

class MazeExample1(Maze):
    """7x7 example maze from lecture 15"""
    def __init__(self):
        """Set blocked cells for 7x7 example from lecture 15"""
        super().__init__(xsize=7, ysize=7, start=(1,1), goal=(5,5))
        self.apply_border()
        for x,y in [ (2,1), (2,2), (3,2), (4,2), (1,4), (2,4), (4,4), (5,4) ]:
            self.set_blocked(x,y)

def tohexcolor(rgbtuple):
    """Convert 8-bit RGB color tuple to hex color"""
    r,g,b = rgbtuple
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

if __name__=="__main__":
    import sys
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    else:
        n = 31
    print("Generating a random {}x{} maze".format(n,n))
    M = PrimRandomMaze(n,n)
    M.save_svg("random_maze.svg")
    print("Saved SVG")
    try:
        M.save_png("random_maze.png",scale=10)
        print("Saved PNG")
    except ImportError:
        print("Not saving PNG maze image, because Pillow / PIL was not found.")
        print("(Install it with a command like 'python3 -m pip install pillow')")
