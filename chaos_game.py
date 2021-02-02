"""
The Chaos Game
Each random die roll plots a point halfway to the corresponding point.

TO RUN PROGRAM:
>>> python chaos_game.py

Example outputs can be seen in chaos1.png, chaos2.png, and chaos3.png.

Last Updated: 2 February 2020
Author: River Veek
"""

import random as r
import turtle as t
import math as m

ITER = 1000  # number of iterations to run program
FAST = 1  # 1 = isntant plotting, 0 = procedural plotting
SIZEX = -300  # size of usable x axis
SIZEY = 300  # size of usable y axis


def roll():
    """
    Simulates die roll (between 1 and 6 inclusize).

    Corresponding letters:
    A = 1, 2
    B = 3, 4
    C = 5, 6
    """
    return r.randint(1, 6)

def rand():
    """
    Returns random number in range SIZEX to SIZEY.

    Called once for the starting four points (three in triangle)
    plus one other.
    """
    return r.randint(SIZEX, SIZEY)

def drawPoint(t, point, color="black"):
    """
    Draws point in space using Turtle Graphics.
    """
    t.pu()
    t.goto(point.x, point.y)
    t.pencolor(color)
    t.dot()

def euclideanDist(p1, p2):
    """
    Returns Euclidean distance between two points

    NO LONGER USED IN THIS PROGRAM.
    """
    return m.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

def getMidpoint(p1, p2):
    """
    Returns tuple representing midpoint between two points.
    """
    return (p1.x + p2.x) / 2, (p1.y + p2.y) / 2

class Point:
    """
    Each instance has x and y location.
    """

    def __init__(self, x, y):
        """
        Constructor.
        """
        self.x = x
        self.y = y


def main(fast=FAST):
    """
    Conducts main logic.

    If FAST is set to 1, plotting will be instant
    """
    window = t.Screen()
    turtle = t.Turtle()

    # fastest speed
    turtle.speed(10)

    if fast == 1:
        window.tracer(0, 0)

    # plot initial points (three plus initial point)
    A = Point(rand(), rand())
    drawPoint(turtle, A, "red")

    B = Point(rand(), rand())
    drawPoint(turtle, B, "red")

    C = Point(rand(), rand())
    drawPoint(turtle, C, "red")

    X = Point(rand(), rand())
    drawPoint(turtle, X,)

    for i in range(ITER):

        # random die roll
        r = roll()

        # plot point halfway from current X to A/B/C
        if r in [1, 2]:
            midpoint = getMidpoint(A, X)
            X.x, X.y = midpoint
            drawPoint(turtle, X)

        elif r in [3, 4]:
            midpoint = getMidpoint(B, X)
            X.x, X.y = midpoint
            drawPoint(turtle, X)

        else:
            midpoint = getMidpoint(C, X)
            X.x, X.y = midpoint
            drawPoint(turtle, X)

    if fast == 1:
        window.update()

    # click to exit (after plotting has finished)
    window.exitonclick()

main()
