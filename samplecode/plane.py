"""2-dimensional vectors and points"""
# MCS 275 Spring 2022 Lecture 4 and Project 3
# THIS VERSION HAS THE UPDATES NEEDED FOR PROJECT 3!
# Emily Dumas

import math

class Vector2:
    """2-dimensional vector"""

    def __init__(self, x, y):
        "Create a new vector with components x,y"
        self.x = x  # make a new attribute of THIS OBJECT called x
        self.y = y

    def __str__(self):
        "Human-readable string representation"
        return "Vector2({},{})".format(self.x, self.y)

    def __repr__(self):
        "Unambiguous string representation"
        return str(self)

    def __mul__(self, scalar):
        "Vector times scalar"
        if isinstance(scalar, float) or isinstance(scalar, int):
            return Vector2(scalar * self.x, scalar * self.y)
        else:
            return NotImplemented

    def __rmul__(self, scalar):
        "scalar times Vector"
        # If A doesn't know how to compute A*B with A.__mul__(B),
        # Python will give B a chance to compute it by calling B.__rmul__(A)
        # This is called a "reflected" multiplication special method
        if isinstance(scalar, float) or isinstance(scalar, int):
            return Vector2(scalar * self.x, scalar * self.y)
        else:
            return NotImplemented

    def __add__(self, other):
        "Vector plus Vector and Vector plus Point"
        if isinstance(other, Vector2):
            # Vector2 + Vector2 is Vector2
            return Vector2(self.x + other.x, self.y + other.y)
        elif isinstance(other, Point2):
            # Vector2 + Point2 is Point2
            return Point2(self.x + other.x, self.y + other.y)
        else:
            return NotImplemented

    def __sub__(self, other):
        "Vector minus Vector"
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        else:
            return NotImplemented

    def __eq__(self, other):
        "Vector equality means component equality"
        if not isinstance(other, Vector2):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def angle(self):
        """
        Returns the angle of the vector, in radians.
        If the vector is zero, raises `ValueError`.
        """
        if self.x == 0 and self.y == 0:
            raise ValueError("Zero vector has no angle")
        theta = math.atan2(self.y, self.x)
        if theta < 0:
            return theta + 2 * math.pi
        else:
            return theta

    def sector(self):
        """
        Which third of the plane contains this vector?
        Returns an integer 0, 1, or 2.
        """
        theta = self.angle()
        theta_turns = theta / (2 * math.pi)
        if theta_turns < (1 / 3):
            return 0
        elif theta_turns < (2 / 3):
            return 1
        else:
            return 2


class Point2:
    """2-dimensional point"""

    def __init__(self, x, y):
        "Create a new point with coordinates x,y"
        self.x = x
        self.y = y

    def __str__(self):
        "Human-readable string representation"
        return "Point2({},{})".format(self.x, self.y)

    def __repr__(self):
        "Unambiguous string representation"
        return str(self)

    def __add__(self, other):
        "Point plus Vector"
        if isinstance(other, Vector2):
            return Point2(self.x + other.x, self.y + other.y)
        else:
            return NotImplemented

    def __eq__(self, other):
        "Point equality means coordinate equality"
        if not isinstance(other, Point2):
            return NotImplemented
        return self.x == other.x and self.y == other.y


    def __sub__(self, other):
        "Point minus Point and Point minus Vector"
        if isinstance(other, Vector2):
            return Point2(self.x - other.x, self.y - other.y)
        elif isinstance(other, Point2):
            return Vector2(self.x - other.x, self.y - other.y)
        else:
            return NotImplemented

    def sector_of(self, other):
        "Determine the sector (0, 1, or 2) that contains the Point2 object `other`"
        return (other - self).sector()
