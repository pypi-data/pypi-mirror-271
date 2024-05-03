"""Image manipulation"""
__version__ = "0.0.1" # 2023.02
__author__ = "S. Gebert <nomisge @ live . de>"
__all__ = ['PImage', 'new_pixel_array', 'new_array', 'Array', 'PixelArray']

from pysideprocessing.pgraphics import PGraphics, Paintable
# import pysideprocessing.pconstants as pc

from PySide6.QtGui import QImage, QPixmap
from typing import Optional, Literal, ClassVar

import numpy as np
import numpy.typing as npt


PixelArray = npt.NDArray[np.uint32]
"""TODO: Beschreibung PixelArray
"""

Array = npt.NDArray

def new_pixel_array(width:int, height: int ) -> PixelArray:
    return np.empty(shape=(width,height),dtype=np.uint32,order='C')

def new_array(array: npt.ArrayLike) -> Array:
    return np.array(array)

class PImage(PGraphics, Paintable):
    
    PIXELS_DIMENSION: ClassVar[Literal[1,2]] = 1 #Dimension der pixels liste
#     COLOR_MODE: Literal[pc.RGB, pc.ARGB] = pc.ARGB
    COLOR_MODE: ClassVar[int] = 2 # pc.RGB = 1 oder pc.ARGB = 2

    _image: QImage
    _pixels: Optional[PixelArray]
    
    #TODO: image formats
    def __init__(self, width:int = -1, height: int = -1, filename: str|QImage = "", format=QImage.Format.Format_ARGB32_Premultiplied):
        if not filename == "":
            if isinstance(filename, QImage):
                self._image = filename
                self._image.convertToFormat(format)
            else:
                self._image = QImage(filename)
        else:
            if width < 0 or height < 0:
                raise ValueError("size constraints cannot be negative")
            self._image = QImage(width, height, format)
        super().__init__(self)
        
    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        result._pixels = None
        return result
    
    def copy(self):
        """A copy of the image, using implicit data sharing (copy-on-write) on the containing QImage"""
        return self.__copy__()

    def get_image(self):
        return self._image
    
    def get_paint_device(self) -> QPixmap|QImage:
        return self._image

    @property
    def pixels(self) -> PixelArray:
        """Bilddaten als ein oder zweidimensionales Pixel-Array.
        
        Returns
        -------
        PixelArray
            zweidimensionales Pixel-Array
        """
        if self._pixels is None:
            raise Exception("pixels not loaded") # TODO meaningful exception
        return self._pixels
    
    @pixels.setter
    def pixels(self, pixels:PixelArray):
        """
        
        Parameters
        ----------
        pixels : array_like
            ein oder zweidimensionales PixelArray
        """
        if self._pixels is None:
            raise Exception("pixels not loaded") # TODO meaningful exception
        self._pixels = pixels.copy()

    @property
    def width(self) -> int:
        return self._image.width()
    @property
    def height(self) -> int:
        return self._image.height()
        
    @property
    def pixmap(self) -> QPixmap:
        return QPixmap.fromImage(self._image)
    
    def load_pixels(self):
        """Läd die Pixel Daten des momentan angezeigten Bilds in die pixels[] Liste.
        """
        #TODO set image format
        
        shape: int|tuple[int,int] = 0 # type: ignore[annotation-unchecked]
        if self.PIXELS_DIMENSION == 1:
            shape=self.height*self.width
            
        if self.PIXELS_DIMENSION == 2:
            shape=(self.height,self.width)
        
        #TODO: return 1D array or 2D array depending on setting
        self._pixels = np.ndarray(shape=shape,dtype=np.uint32, buffer=self._image.bits(),order='C')
        if self.PIXELS_DIMENSION == 2:
            self._pixels = np.swapaxes(self._pixels,0,1)     
        
    def update_pixels(self, width = -1, height = -1):
        """Setzt das Bild neu auf Basis des Pixel-Arrays.

        Die Groesse des Bildes wird nicht automatisch an das Array angepasst.
        """
        if self._pixels is None:
            raise Exception("pixels not loaded") # TODO meaningful exception
        
        if width < 0: width = self.width
        if height < 0: height = self.height
        
        self._image = QImage(bytes(np.swapaxes(self._pixels,0,1)), width, height, QImage.Format.Format_ARGB32_Premultiplied)

    
    def save(self, filename: str, format: Optional[bytes]=None, quality:int=-1):
        """Speichert ein Bild.

        Speichert ein Bild auf einem Datentraeger. Zulaessig sind die Dateiformate PNG und GIF. Die Dateiendung legt den Typ fest.
        Standardmaessig wird die Dateiendung .png ergaenzt, wenn keine angegeben ist.
        
        Parameters
        ----------
        filename : str
            Dateiname des Bildes
        format : str, optional
        quality : int, optional
        """
        self._image.save(filename, format, quality)