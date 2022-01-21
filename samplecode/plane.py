"""2-dimensional vectors and points"""
# MCS 275 Spring 2022 Lecture 4 (w/ post-lecture add-ons)

# If A is an instance of class Foo
# A.stuff(5,6,28)
# -->
# Foo.stuff(A,5,6,28) 
#           \---- self

class Vector2:
    """2-dimensional vector"""
    def __init__(self,x,y):
        "Create a new vector with components x,y"
        self.x = x # make a new attribute of THIS OBJECT called x
        self.y = y

    def __str__(self):
        "Human-readable string representation"
        return "Vector2({},{})".format(self.x,self.y)

    def __repr__(self):
        "Unambiguous string representation"
        return str(self)

    def __mul__(self,scalar):
        "Vector times scalar"
        if isinstance(scalar,float) or isinstance(scalar,int):
            return Vector2(scalar*self.x,scalar*self.y)
        else:
            return NotImplemented

    def __rmul__(self,scalar):
        "scalar times Vector"
        # If A doesn't know how to compute A*B with A.__mul__(B),
        # Python will give B a chance to compute it by calling B.__rmul__(A)
        # This is called a "reflected" multiplication special method
        if isinstance(scalar,float) or isinstance(scalar,int):
            return Vector2(scalar*self.x,scalar*self.y)
        else:
            return NotImplemented

    def __add__(self,other):
        "Vector plus Vector and Vector plus Point"
        if isinstance(other,Vector2):
            # Vector2 + Vector2 is Vector2
            return Vector2(self.x+other.x,self.y+other.y)
        elif isinstance(other,Point2):
            # Vector2 + Point2 is Point2
            return Point2(self.x+other.x,self.y+other.y)
        else:
            return NotImplemented

    def __sub__(self,other):
        "Vector minus Vector"
        if isinstance(other,Vector2):
            return Vector2(self.x-other.x,self.y-other.y)
        else:
            return NotImplemented

    def __eq__(self,other):
        "Vector equality means component equality"
        if not isinstance(other,Vector2):
            return NotImplemented
        return self.x==other.x and self.y==other.y

    def __abs__(self):
        return (self.x**2 + self.y**2)**0.5

class Point2:
    """2-dimensional point"""
    def __init__(self,x,y):
        "Create a new point with coordinates x,y"
        self.x = x
        self.y = y

    def __str__(self):
        "Human-readable string representation"
        return "Point2({},{})".format(self.x,self.y)

    def __repr__(self):
        "Unambiguous string representation"
        return str(self)

    def __add__(self,other):
        "Point plus Vector"
        if isinstance(other,Vector2):
            return Point2(self.x+other.x,self.y+other.y)
        else:
            return NotImplemented

    # self - other
    # -->
    # self.__sub__(other)
    def __sub__(self,other):
        "Point minus Point and Point minus Vector"
        if isinstance(other,Vector2):
            return Point2(self.x-other.x,self.y-other.y)
        elif isinstance(other,Point2):
            return Vector2(self.x-other.x,self.y-other.y)
        else:
            return NotImplemented