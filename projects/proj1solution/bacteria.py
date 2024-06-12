# MCS 275 Spring 2022 Project 1 Solution
# Emily Dumas
"Bacteria classes for simulation"

from plane import Vector2, Point2

class Bacterium:
    "Base class for bacteria living in an Environment"
    def __init__(self, env, position):
        "Initialize a bacterium at `position` (a Point2) and add to Environment `env`"
        self.env = env
        self.alive = True
        self.position = position
        if not self.env.is_available(position):
            raise ValueError("Specified position not available")
        self.env.add(self)

    def can_move(self, v):
        "Is it allowable for this bacterium to move by Vector2 `v`?"
        return self.env.is_available(self.position + v)

    def move(self, v):
        "Move by Vector2 `v`"
        self.position += v

    def nutrients_available(self, v=Vector2(0, 0)):
        """
        Return quantity of nutrients available at the bacterium's position.
        Or, if a vector `v` is given, return the quantity available at
        position+v.
        """
        return self.env.get_nutrients(self.position + v)

    def consume(self, k):
        """
        Consume `k` nutrients at the current position (raises ValueError
        if not enough nutrients are available.
        """
        self.env.consume_nutrients(self.position, k)

    def die(self):
        "Make this bacterium die"
        self.alive = False

    def update(self):
        "Advance the simulation one time step (by doing nothing)"
        # Subclasses should override this method to do things!

    def __str__(self):
        "Human-readable string representation used by `print`"
        return "{}(position=({},{}))".format(self.__class__.__name__,self.position.x,self.position.y)

    def __repr__(self):
        "Unambiguous string representation used in the REPL"
        return str(self)


# -- classes added as part of project 1 appear below --

class Eater(Bacterium):
    """
    Bacterium that eats until nutrients are exhausted, then tries to move
    to a neighboring grid square that has nutrients.  If it cannot do
    so, it dies.
    """
    # Possible motion considered when we run out of nutrients
    moves = (Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1))

    def update(self):
        "Eat, move, or die"
        try:
            self.consume(1)
        except ValueError:
            # Can't consume, so try to move instead
            for v in self.moves:
                if self.can_move(v) and self.nutrients_available(v) > 0:
                    # Found a way to go, so move there and return
                    self.move(v)
                    return
            
            # It we get here, it means we didn't find anywhere to go
            self.die()
        


class Floater(Bacterium):
    """
    Bacterium that always tries to decrease its y coordinate.  If it cannot do this,
    it just pauses and consumes one unit of nutrients.  If it pauses but there are
    no nutrients available, it dies.
    """
    # Relative position that is considered "up" in this simulation
    up = Vector2(0, -1)

    def update(self):
        "Float up, eat, or die"
        if self.can_move(self.up):
            self.move(self.up)
            return

        # If we reach this point, it wasn't possible to move up.
        # So we eat or die.
        try:
            self.consume(1)
        except ValueError:
            self.die()


class Divider(Bacterium):
    """
    Bacterium that can divide if its current location is sufficiently nutrient-rich 
    and if there is space available in a neighboring grid square.  Doing so consumes
    3 units of nutrients.
    """
    # Places we'll check for division (order is important)
    neighbors = (Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1))

    def update(self):
        "Divide if there are sufficient nutrients and space, otherwise eat or die"
        here = self.nutrients_available()
        if here >= 3:
            # There are plenty of nutrients, so we should check for an available
            # spot and divide if one is found.
            available_neighbor = None
            for v in self.neighbors:
                if self.can_move(v):
                    available_neighbor = v
                    break # stop searching as soon as first available spot is found

            if available_neighbor:
                # We have nutrients and room, so divide!
                self.consume(3)
                Divider(self.env, self.position + available_neighbor)
                return
    
        # If we reach this point, it means we didn't meet the conditions to
        # divide, so we're supposed to consume one nutrient point or die.
        try:
            self.consume(1)
        except ValueError:
            self.die()
