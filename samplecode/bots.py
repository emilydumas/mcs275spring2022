"""Classes representing robots in a simulation"""
# MCS 275 Spring 2022 David Dumas
# Lecture 5

import plane
import random

class Bot:
    """Base class for all robots.  Sits in one place forever."""
    def __init__(self,position):
        """Setup with initial position `position` (a plane.Point2 instance)"""
        self.alive = True
        if not isinstance(position,plane.Point2):
            raise TypeError("`postition` must be a Point2")
        self.position = position # intended to be a plane.Point2 instance
    
    def __str__(self):
        """Human-readable string representation"""
        return "{}(position=({},{}),alive={})".format(self.__class__.__name__,self.position.x,self.position.y,self.alive)

    def __repr__(self):
        """Unambiguous string representation"""
        return str(self)

    def update(self):
        """Advance one time step (by doing nothing)"""

class WanderBot(Bot):
    """A robot that wanders randomly"""
    def update(self):
        """Take one random step"""
        steps = [ plane.Vector2(1,0), plane.Vector2(-1,0), plane.Vector2(0,1), plane.Vector2(0,-1) ]
        self.position = self.position + random.choice(steps)

