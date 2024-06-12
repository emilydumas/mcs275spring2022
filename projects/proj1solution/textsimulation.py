# MCS 275 Spring 2022 - Instructor Emily Dumas
# Project 1 solution
import os
import sys
from plane import Point2, Vector2
from bacteria import *
from environments import Environment, HillEnvironment, GradientEnvironment

if "--fancy" in sys.argv[1:]:
    bar = " \u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588"
else:
    bar =  " .,:;il#@"

def show_environment(S):
    """
    Print text-graphics representation of an environment where bacteria
    are represented by the first letters of their class names.
    """
    for y in range(S.height):
        for x in range(S.width):
            for o in S.organisms:
                if o.position.x == x and o.position.y == y:
                    print(o.__class__.__name__[0], end="")
                    break
            else:
                print(
                    bar[S.get_nutrients(Point2(x, y))],
                    end="",
                )
        print()

# Create an environment
# (Also try Environment or GradientEnvironment)
S = HillEnvironment(40, 8)

Eater(S, Point2(3, 3))
Floater(S, Point2(18, 6))
Floater(S, Point2(10, 5))
Divider(S, Point2(0, 7))
Divider(S, Point2(7, 0))
Divider(S, Point2(20, 3))

# Run and display the simulation
t = 0
while True:
    os.system("cls||clear") # This clears the screen in windows, macos, or linux
    print("Bacterial simulation in {}x{} environment".format(S.width,S.height))
    print()
    show_environment(S)
    print("\n{} steps, {} organisms alive".format(t,len(S.organisms)))
    input("ENTER for next time step")
    S.update()
    t+=1
