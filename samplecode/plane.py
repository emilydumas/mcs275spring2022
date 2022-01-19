"""2-dimensional vectors and points"""
# MCS 275 Spring 2022 Lecture 4

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
    def __add__(self,other):
        "Vector-Vector and Vector-Point addition"
        print("Hello from Vector2.__add__!")
        if isinstance(other,Vector2):
            # Vector2 + Vector2 is Vector2
            return Vector2(self.x+other.x,self.y+other.y)
        elif isinstance(other,Point2):
            # Vector2 + Point2 is Point2
            return Point2(self.x+other.x,self.y+other.y)
        else:
            return NotImplemented

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
        "Point plus Vector addition"
        if isinstance(other,Vector2):
            return Point2(self.x+other.x,self.y+other.y)
        else:
            return NotImplemented

    # self - other
    # -->
    # self.__sub__(other)
    def __sub__(self,other):
        "Point minus Point is a Vector"
        if isinstance(other,Point2):
            return Vector2(self.x-other.x,self.y-other.y)
        else:
            return NotImplemented