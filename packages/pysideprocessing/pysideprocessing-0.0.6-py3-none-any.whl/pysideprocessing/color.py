"""Color handling"""
__version__ = "0.0.1" # 2023.02
__author__ = "S. Gebert <nomisge @ live . de>"
__all__ = ['color', 'alpha', 'red', 'green', 'blue']

import numpy as np
from numba import njit # type: ignore[import]
from numba.extending import overload # type: ignore[import]
from numba.core.errors import TypingError, NumbaExperimentalFeatureWarning # type: ignore[import]

from typing import cast

#ignore warning of isinstance beeing numba experimental
import warnings
warnings.simplefilter('ignore', category=NumbaExperimentalFeatureWarning)


from PySide6.QtGui import QColor

class color(int):
    """Creates colors for storing in variables of the color datatype.

    The parameters are interpreted as RGB or HSB values depending on the current colorMode().
    The default mode is RGB values from 0 to 255 and,
    therefore, color(255, 204, 0) will return a bright yellow color (see the first example above).

    Note that if only one value is provided to color(), it will be interpreted as a grayscale value.
    Add a second value, and it will be used for alpha transparency.
    When three values are specified, they are interpreted as either RGB or HSB values.
    Adding a fourth value applies alpha transparency.
    
    Syntax
    ------
    color(gray)
    color(gray,alpha)
    color(red,green,blue)
    color(red,green,blue,alpha)
    
    Parameters
    ----------
    v1: int
        if optional parameters v2, v3 and a not used: number specifying value between white and black
        else red or hue values relative to the current color range
    v2: int, optional
        if optional parameters v3 and a not used: alpha relative to current color range
        else green or saturation values relative to the current color range
    v3: int, optional
        blue or brightness values relative to the current color range
    a: int, optional
        alpha relative to current color range
    
    """
    _color_value:int
    
    def __new__(cls, v1: int|str, v2: int = -1, v3: int = -1, a: int = -1):
        #TODO: bound checks on parameters depending on set color range
        # TODO: color range should be specifiable via a color mode setting;
        # COLOR_MODE rgb/hsv not needed, use QColor methods instead
        if isinstance(v1, str):
            return QColor.fromString(v1).rgba()
        if v3 < 0:
            if v2 > 0:
                a = v2
            if v1 >= 0 and v1 <= 255:
                v2 = v1
                v3 = v1
            else:
                return v1
                    
        if a < 0: a = 0xff
        return (a << 24) | (v1 << 16) | (v2 << 8) | (v3)
    
#     def __init__(self, v1: int|str, v2: int = -1, v3: int = -1, a: int = -1):
#         if isinstance(v1, str):
#             self._color_value = QColor.fromString(v1).rgba()
#             return
#         if v3 < 0:
#             if v2 > 0:
#                 a = v2
#             if v1 >= 0 and v1 <= 255:
#                 v2 = v1
#                 v3 = v1
#             else:
#                 self._color_value = v1
#                 return            
#         if a < 0: a = 0xff
#         self._color_value = (a << 24) | (v1 << 16) | (v2 << 8) | (v3)
#     
#     def __int__(self) -> int:
#         return self._color_value
#     
#     def __lshift__(self, other) -> int:
#         if not isinstance(other, int):
#             raise ValueError("Argument must be integer")
#         return int(self) << other
#     def __rlshift__(self, other) -> int:
#         if not isinstance(other, int):
#             raise ValueError("Argument must be integer")
#         return other << int(self)
#         
#     def __rshift__(self, other) -> int:
#         if not isinstance(other, int):
#             raise ValueError("Argument must be integer")
#         return int(self) >> other
#     
#     def __rrshift__(self, other) -> int:
#         if not isinstance(other, int):
#             raise ValueError("Argument must be integer")
#         return other >> int(self)
#     
#     def __and__(self, other) -> int:
#         if not isinstance(other, int):
#             raise ValueError("Argument must be integer")
#         return int(self) & other
#     
#     def __rand__(self, other) -> int:
#         if not isinstance(other, int):
#             raise ValueError("Argument must be integer")
#         return int(self) & other
        
    #TODO: pythonic names and docstring
    @classmethod
    def fromRgb(cls, r:int,g:int,b:int,a:int=255):
        """TODO: for now - test docstring """
        return QColor.fromRgb(r,g,b,a).rgba()
    @classmethod
    def getHsl(cls, color_value:"color"):
        return QColor(color_value).getHsl()
    @classmethod
    def getRgb(cls, color_value:"color"):
        return QColor(color_value).getRgb()

@overload(color)
def impl_color(v1: int, v2: int = -1, v3: int = -1, a: int = -1):
    def impl(v1: int, v2: int = -1, v3: int = -1, a: int = -1) -> int|np.uint32:
        #TODO implement bound checks on parameters
        if not isinstance(v1, (int,np.uint32)):
            raise TypingError("v1 must be a scalar int|uint32")
        if v3 < 0:
            if v2 > 0:
                a = v2
            if v1 >= 0 and v1 <= 255:
                v2 = v1
                v3 = v1
            else:
                return v1
                
        if a < 0: a = 0xff
        return (a << 24) | (v1 << 16) | (v2 << 8) | (v3)
    return impl

def lerp_color(c1: int, c2: int, amt: float):
    """Calculates a color between two colors at a specific increment.

    The amt parameter is the amount to interpolate between the two values where 0.0 is equal to the first point, 0.1 is very near the first point, 0.5 is halfway in between, etc.
    An amount below 0 will be treated as 0. Likewise, amounts above 1 will be capped at 1. This is different from the behavior of lerp(), but necessary because otherwise numbers outside the range will produce strange and unexpected colors.

    Parameters
    ----------
    c1: int
        interpolate from this color
    c2: int
        interpolate to this color
    amt: float
        between 0.0 and 1.0
    """
    raise NotImplementedError()

@njit
def alpha(color_value: color) -> int:
    return 0xff & (color_value >> 24)

@njit
def red(color_value: color) -> int:
    """Extracts the red value from a color, scaled to match current colorMode().

    The value is always returned as a float, so be careful not to assign it to an int value.
    
    Parameters
    ----------
    color_value: PColor
        any value of the color datatype
    """
    return 0xff & (color_value >> 16)
 
@njit
def green(color_value: color) -> int:
    """Extracts the green value from a color, scaled to match current colorMode().

    The value is always returned as a float, so be careful not to assign it to an int value.
    
    Parameters
    ----------
    color_value: PColor
        any value of the color datatype
    """
    return 0xff & (color_value >> 8)

@njit
def blue(color_value: color) -> int:
    """Extracts the blue value from a color, scaled to match current colorMode().

    The value is always returned as a float, so be careful not to assign it to an int value.
    
    Parameters
    ----------
    color_value: PColor
        any value of the color datatype
    
    Returns
    -------
    
    """
    return 0xff & color_value

def saturation(color_value: color) -> float:
    """Extracts the saturation value from a color.
    
    Parameters
    ----------
    color_value: PColor
        any value of the color datatype
    """
    raise NotImplementedError() 