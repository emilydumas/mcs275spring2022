"""Robot motion simulation with simple text-based graphics"""
# MCS 275 Spring 2022 Emily Dumas
# Lecture 5

from plane import Vector2,Point2
import bots
import random

width=60
height=30

current_bots = []
for i in range(5):
    P = Point2(random.randint(0,width-1),random.randint(0,height-1))
    current_bots.append(bots.WanderBot(position=P))

current_bots.append(bots.DestructBot(position=Point2(3,3),lifetime=5))
current_bots.append(bots.DestructBot(position=Point2(1,28),lifetime=7))
current_bots.append(
    bots.PatrolBot(position=Point2(8,8),step=Vector2(1,1),numsteps=3)
    )
n=0
while True:
    print("\n"*3*height)
    board = [ [" "]*width for _ in range(height) ]
    for b in current_bots:
        if not b.alive:
            continue
        elif b.position.x < 0 or b.position.x >= width:
            continue
        elif b.position.y < 0 or b.position.y >= height:
            continue
        board[b.position.y][b.position.x] = "*" # TODO: Mark each bot with a different letter!
    for row in board:
        print("".join(row))
    print("time={}".format(n))
    input()

    for b in current_bots:
        b.update()
    n += 1
