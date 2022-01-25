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

    def move(self,v):
        "Move the position of this Bot by Vector2 `v`"
        self.position = self.position + v

    def __str__(self):
        """Human-readable string representation"""
        return "{}(position=({},{}),alive={})".format(
            self.__class__.__name__,
            self.position.x,
            self.position.y,
            self.alive
        )

    def __repr__(self):
        """Unambiguous string representation"""
        return str(self)

    def update(self):
        """Advance one time step (by doing nothing)"""


class WanderBot(Bot):
    """A robot that wanders randomly"""
    steps = [ plane.Vector2(1,0), plane.Vector2(-1,0), plane.Vector2(0,1), plane.Vector2(0,-1) ]
    def update(self):
        """Take one random step"""
        self.move(random.choice(self.steps))


class HorizontalWanderBot(WanderBot):
    """A robot that wanders randomly along a horizontal line"""
    # Because we inherit from WanderBot, all we need to do is
    # change the value of class attribute `steps`.
    steps = [ plane.Vector2(1,0), plane.Vector2(-1,0) ]


class DestructBot(Bot):
    """A robot that sits for a while and then self-destructs"""
    def __init__(self,position,lifetime):
        """
        Initialize bot with position `position` (Point2) and
        which will sit there for `lifetime` steps
        """
        # super() # returns an object that behaves like self, but
                 # is a Bot, not a DestructBot
        super().__init__(position)  # call constructor of Bot
        self.lifetime = lifetime
        self.remaining = self.lifetime
        if self.lifetime <= 0:
            self.alive = False

    def __str__(self):
        """Human-readable string representation"""
        return "{}(position=({},{}),lifetime={},remaining={})".format(
            self.__class__.__name__,
            self.position.x,
            self.position.y,
            self.lifetime,
            self.remaining
        )

    def update(self):
        "Sit still and possibly self-destruct"
        if not self.alive:
            return
        self.remaining -= 1
        if self.remaining <= 0:
            # self-destruct
            self.alive = False

class PatrolBot(Bot):
    """A robot walks back and forth forever"""
    def __init__(self,position,step,numsteps):
        """
        Initialize a PatrolBot starting at `position`,
        taking steps given by Vector2 `step`, and turning
        around after `numsteps` steps.
        """
        super().__init__(position)
        self.step = step
        self.numsteps = numsteps
        self.curstep = 0

    def __str__(self):
        """Human-readable string representation"""
        return "{}(position=({},{}),step={},numsteps={},curstep={})".format(
            self.__class__.__name__,
            self.position.x,
            self.position.y,
            self.step,
            self.numsteps,
            self.curstep
        )

    def update(self):
        "Take one step and possibly turn around"
        if self.curstep == self.numsteps:
            self.step = -1*self.step # reverse direction
            self.curstep = 0 # reset the step counter
        self.move(self.step)
        self.curstep += 1


