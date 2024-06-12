# MCS 275 Spring 2022 - Instructor Emily Dumas
# Project 1 starter pack
from plane import Point2, Vector2
import math

class Environment:
    def __init__(self, width, height, initial_nutrients=8):
        self.width = width
        self.height = height
        self.organisms = []
        self.nutrients = [
            [initial_nutrients for y in range(height)] for x in range(width)
        ]
        self.organism_list_frozen = False
        self.organism_waiting_list = []

    # -------------------------------------------------------------------------
    # PUBLIC METHODS - use these!
    # -------------------------------------------------------------------------

    def is_valid_position(self, p):
        "Is the Point2 `p` an allowed grid position?"
        return p.x >= 0 and p.x < self.width and p.y >= 0 and p.y < self.height

    def is_available(self, p):
        "Is the Point2 `p` valid and unoccupied?"
        return self.is_valid_position(p) and not self.organism_at(p)

    def get_nutrients(self, p):
        "Return the nutrient quantity at Point2 `p`"
        return self.nutrients[p.x][p.y]

    def set_nutrients(self, p, k):
        "Set the nutrient quantity at Point2 `p` to `k`"
        self.nutrients[p.x][p.y] = k

    def consume_nutrients(self, p, k):
        """
        Decrease the nutrient quantity at Point2 `p` by `k`, raising a
        ValueError if the result would be negative.
        """
        cur = self.get_nutrients(p)
        if cur >= k:
            self.set_nutrients(p, cur - k)
        else:
            raise ValueError(
                "Insufficent nutrients at {}: attempted to consume {} when {} present".format(p, k, cur)
            )

    def add(self, o):
        "Add the organism object `o` to this environment."
        # It's possible we might be in the process of doing an update()
        # in which case we can't add the organism immediately.  In that
        # case it goes in a waiting list.
        if o in self.organisms or o in self.organism_waiting_list:
            raise ValueError("Attempted to add organism {} which had already been added to this environment.".format(o))
        if self.organism_list_frozen:
            self.organism_waiting_list.append(o)
        else:
            self.organisms.append(o)

    def update(self):
        """
        Advance the simulation one unit of time, calling .update()
        on every organism and then culling dead organisms.
        """
        # We don't want to modify the list of organisms while iterating
        # over it, so we freeze it for now.
        self.freeze_organism_list()
        # Call .update() on each organism
        for o in self.organisms:
            o.update()
        # Remove dead organisms
        self.organisms = [o for o in self.organisms if o.alive == True]
        # Unpause addition of new organisms and handle waiting list
        self.unfreeze_organism_list()

    # -------------------------------------------------------------------------
    # PRIVATE METHODS - do not use, no need to read
    # -------------------------------------------------------------------------

    def organism_at(self, p):
        "Return the organism object at Point2 `p`, or None"
        for o in self.organisms:
            if o.position == p:
                return o
        return None

    def freeze_organism_list(self):
        "Temporarily pause addition of new organisms (use waiting list)"
        self.organism_list_frozen = True

    def unfreeze_organism_list(self):
        "Unpause addition of organisms and handle waiting list"
        self.organism_list_frozen = False
        for o in self.organism_waiting_list:
            self.organisms.append(o)
        self.organism_waiting_list.clear()

    def __str__(self):
        "Human-readable string representation used by `print`"
        return "{}(width={},height={})".format(self.__class__.__name__,self.width,self.height)

    def __repr__(self):
        "Unambiguous string representation used in the REPL"
        return str(self)

# =============================================================================
# Subclasses of Environment that create different nutrient densities
# =============================================================================

class GradientEnvironment(Environment):
    "An Environment with lots of nutrients at the bottom, less on top"

    def __init__(self, width, height):
        "Set up environment with vertical nutrient gradient"
        super().__init__(width, height, 0)
        for x in range(width):
            for y in range(height):
                # This formula means 0 at top, 8 at bottom
                self.set_nutrients(Point2(x, y), min(8,(9 * y) // (self.height - 1)))


class HillEnvironment(Environment):
    "An Environment with lots of nutrients near the center, less on the edges"

    def __init__(self, width, height):
        "Set up environment with central nutrient gradient"
        super().__init__(width, height, 0)
        center = Point2((width - 1) / 2, (height - 1) / 2)
        inradius = max(center.x, center.y)
        for x in range(width):
            for y in range(height):
                # This formula uses a "bell curve" to make 1 at the edges and 8
                # at the center.
                p = Point2(x, y)
                z = 9 * math.exp(-1.5 * abs(p - center) ** 2 / inradius ** 2)
                self.set_nutrients(p, max(1, min(8, int(z))))
