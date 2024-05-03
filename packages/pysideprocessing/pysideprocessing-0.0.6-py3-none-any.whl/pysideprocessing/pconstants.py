"""constants used throughout the project"""
__version__ = "0.0.1" # 2023.02
__author__ = "S. Gebert <nomisge @ live . de>"

# from enum import Enum

"""Numbers shared throughout pysideprocessing module

"""
import math

PI: float = math.pi
"""**PI** is a mathematical constant with the value 3.1415927.

It is the ratio of the circumference of a circle to its diameter. It is useful in
combination with the trigonometric functions **sin()** and **cos()**.
"""

HALF_PI: float = math.pi/2
"""**HALF_PI** is a mathematical constant with the value 1.5707964.

It is half the ratio of the circumference of a circle to its diameter. It is useful in
combination with the trigonometric functions **sin()** and **cos()**.
"""

THIRD_PI: float = math.pi/3
QUARTER_PI: float = math.pi/4
"""**QUARTER_PI** is a mathematical constant with the value 0.7853982.

It is on quarter the ratio of the circumference of a circle to its diameter. It is useful in
combination with the trigonometric functions **sin()** and **cos()**.
"""

TWO_PI: float = math.pi * 2
"""**TWO_PI** is a mathematical constant with the value 6.2831855.

It is twice the ratio of the circumference of a circle to its diameter. It is useful in
combination with the trigonometric functions **sin()** and **cos()**.
"""

TAU: float = math.pi * 2
"""**TAU** is a mathematical constant with the value 6.2831855.

It is the circle constant relating the circumference of a circle to its linear
dimension, the ratio of the circumference of a circle to its radius. It is
useful in combination with trigonometric functions such as **sin()** and **cos()**.
"""

DEG_TO_RAD: float = PI/180
RAD_TO_DEG: float = 180/PI

## Color Mode for colors and/or images
#propably not needed

RGB: int = 1 #image & color
ARGB: int  = 2 #image & color?
HSB: int   = 3 #color
ALPHA: int = 4 #image
CMYK: int = 5 #image & color

### SHAPES

## shape drawing modes
# class ShapeDrawingMode(Enum):
"""Shape drawing modes"""
    
CORNER = 0
"""Draw mode convention to use (x, y) to (width, height)"""

CORNERS = 1
"""Draw mode convention to use (x1, y1) to (x2, y2) coordinates"""

RADIUS = 2
"""Draw mode convention to draw from the center, and using the radius"""

CENTER = 3
"""Draw mode convention to draw from the center, using second pair of values as the diameter."""

DIAMETER = 3
"""Draw mode convention to draw from the center, using second pair of values as the diameter.

Synonym for the CENTER constant
"""

## arc drawing modes
CHORD: int = 2
PIE: int = 3


