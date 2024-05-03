"""Used for oop mode"""
__version__ = "0.0.1" # 2023.02
__author__ = "S. Gebert <nomisge @ live . de>"
__all__ = ['PWidget', 'PSurface','PWidgetMeta']

from pysideprocessing.pimage import PImage, PixelArray
from pysideprocessing.color import color
from pysideprocessing.pgraphics import PGraphics, Graphics, Paintable

from abc import abstractmethod, ABC
from typing import Optional, Callable
from functools import wraps

from PySide6.QtWidgets import QMainWindow, QLabel
from PySide6.QtCore import Property, QTimer, QRect, Qt, QObject
from PySide6.QtGui import QPainter, QPixmap, QImage, QPaintEvent

from collections import deque

# from typing import TypeVar, Generic

# T = TypeVar("T")
# 
# class UndoRedo(Generic[T]):
# 
#     HISTORY_SIZE: int = 2 # Anzahl rückgängig machbarer Schritte
#     _history: deque[T]
# 
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._history = deque()
#     
#     @property
#     def history(self) -> deque[T]:
#         """the history of the states"""
#         return self._history
#     @history.setter
#     def history(self, history):
#         self._history = history
#       
#     @abstractmethod
#     def undo(self):
#         """for undoing the history of the states"""
#     @abstractmethod
#     def redo(self):
#         """for redoing the history of the states"""

class _ShibokenObjectTypeFence(type(QObject)): # type: ignore[misc]
    """
    This solve for:
        TypeError: Shiboken.ObjectType.__new__(PWidgetMeta) is not safe, use type.__new__()

    Principle is to "please" the check done in Objects/typeobject.c:tp_new_wrapper function by
    making look like the "most derived base that's not a heap type" has the same tp_new function
    than Shiboken.ObjectType.

    Another way could have been to declare PWidgetMeta with type(QWidget) first.
    But if you do that, ABCMeta.__new__ is not called, and its internal states do not get properly
    initialised. (Same for any other metaclass you may want to use actually.)
    I guess because Shiboken.ObjectType is not cooperative and does not call the __new__ of
    super types.

    Inserting such "fence" type at the beginning of the metaclass MRO works because:
    - tp_new_wrapper will be happy, and not throw the "not safe" error.
    - As type(QWidget) is also declared further down the MRO, its final (and unique) position in
      the MRO will be that later one, instead of right after the position of this fence type.
      Meaning we still get to normally call other metaclasses __new__ before reaching
      Shiboken.ObjectType.__new__
    """
    ...
    #source: https://bugreports.qt.io/browse/PYSIDE-1767

class PWidgetMeta(_ShibokenObjectTypeFence, type(ABC), type(QObject)): # type: ignore[misc]
    """
    This solve for:
        TypeError: metaclass conflict: the metaclass of a derived class
        must be a (non-strict) subclass of the metaclasses of all its bases
    """
    ...
    #source: https://bugreports.qt.io/browse/PYSIDE-1767

class PaintableGraphicsLabel(Paintable, Graphics, QLabel, metaclass=PWidgetMeta):
    HISTORY_SIZE: int = 2 # Anzahl rückgängig machbarer Schritte
    _history: deque[QPixmap]

    def __new__(cls, *args, **kwargs):
        '''
        This solve for abstraction check not being done by Shiboken.Object.
        Normally, abstraction check is is done by Objects/typeobject.c:object_new.
        NB: cls.__abstractmethods__ is set and populated by ABCMeta.__new__ already.
        '''
        if cls.__abstractmethods__:
            s = 's' if len(cls.__abstractmethods__) > 1 else ''
            raise TypeError(
                f'Can\'t instantiate abstract class {cls.__name__} '
                f'with abstract method{s} {", ".join(cls.__abstractmethods__)}'
            )

        return super().__new__(cls, *args, **kwargs)
    #source: https://bugreports.qt.io/browse/PYSIDE-1767
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._history = deque()
    
    @property
    def history(self) -> deque[QPixmap]:
        """the history of the states"""
        return self._history
    @history.setter
    def history(self, history):
        self._history = history
      
    @abstractmethod
    def undo(self):
        """for undoing the history of the states"""
    @abstractmethod
    def redo(self):
        """for redoing the history of the states"""



def image_modification(method: Callable[...,None]) -> Callable[...,None]:
    @wraps(method)
    def _impl(self,*method_args, **method_kwargs):
        self.push_image()
        method(self,*method_args, **method_kwargs)
        self.update_image()
    return _impl  

class PWidget(PaintableGraphicsLabel, metaclass=PWidgetMeta):
    """Base class for all Sketches that use...
    """
        
    #maybe not use QLabel but other widget that has QPixmap
    _pixmap: QPixmap #das aktuelle Bild
    _image: Optional[PImage]
    _pixels: PixelArray

    _painter: QPainter
    _graphics: PGraphics
   
    # Zoom Faktor
    zoom_factor: float
    ZOOM_FIT: int = -1 #FIT = -1;
    ZOOM_NORMAL: int  = 1#NORMAL = 1;
  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._image = None
        self.zoom_factor = 1        
        self._pixmap = QPixmap()
        
        self.resize(self._pixmap.size())
        
        self._graphics = PGraphics(self)
        self._painter = self._graphics.painter
        self._graphics.background(0xffd3d3d3)

    def setup(self):
        """setup-Methode
        """
        raise NotImplementedError()
    
    def draw(self):
        """draw-Methode
        """
        ...
#         raise NotImplementedError()
    
    @Property(int) # type: ignore[operator]
    def width(self) -> int:
        return self._pixmap.width()
    @Property(int) # type: ignore[operator]
    def height(self) -> int:
        return self._pixmap.height()
       
    @image_modification
    def set_size(self, width: int, height: int):
        self._image = None
        oldpix = self._pixmap.copy(0,0,width,height)
        self._pixmap = QPixmap(width, height)
        self._graphics.clear() #don't change background color, only fill background
        self.resize(self._pixmap.size())
        self._painter.begin(self._pixmap)
        self._painter.drawPixmap(0,0,oldpix)
        self._painter.end()
        
    @property
    def pixels(self) -> PixelArray:
        """Bilddaten als ein oder zweidimensionales Pixel-Array.
        
        Returns
        -------
        list[list[QColor]]
            zweidimensionales QColor-Array
        """
        if self._image is None:
            raise Exception("Image not loaded")
        return self._image.pixels
    
    @pixels.setter
    def pixels(self, pixels:PixelArray):
        """
        
        Parameters
        ----------
        pixels : array_like
            ein oder zweidimensionales Array von QColor-Objekten
        """
        if self._image is None:
            raise Exception("Image not loaded")
        self._image.pixels  = pixels
 
    def load_pixels(self):
        """Läd die Pixel Daten des momentan angezeigten Bilds in die pixels[] Liste.
        """
        self._image = PImage(filename= self._pixmap.toImage())
        self._image.load_pixels()
        #TODO set image format
        
    def update_pixels(self):
        """Setzt das Bild neu auf Basis des Pixel-Arrays.

        Die Groesse des Bildes wird nicht automatisch an das Array angepasst.
        """
        if self._image is None:
            raise Exception("pixels not loaded") # TODO meaningful exception
        
        self.push_image()
        self._image.update_pixels()
        self._pixmap = QPixmap.fromImage(self._image.get_image())
        self.update_image()
   
    def paintEvent(self, e: QPaintEvent):
        super().paintEvent(e)
        self.setPixmap(self._pixmap)
        
    def push_image(self):
        """Speichert das aktuell angezeigte Bild in der history
        """
        if self.HISTORY_SIZE > 0:
            if len(self.history) == self.HISTORY_SIZE:
                self.history.popleft()
            self.history.append(self._pixmap.copy())

    def update_image(self):
        self.update()

    def undo(self):
        """Ruft das letzte abgespeicherte Bild aus der History wieder auf.
        """
        if len(self.history) > 0:
            self._pixmap = self.history.pop()
            self.update()
            
    def redo(self):
        raise NotImplementedError()
    
    def set_pixmap(self, pixmap: QPixmap, save_old_image: bool = False):
        if save_old_image:
            self.push_image()
        self._pixmap = pixmap
        self.resize(self._pixmap.size())
        self.update_image()
    
    def get_pixmap(self) -> QPixmap:
        return self._pixmap
    
    def get_paint_device(self) -> QPixmap|QImage:
        return self._pixmap
    
    def get_image(self) -> PImage:     
        return PImage(filename=self._pixmap.toImage())
    
    def set_zoom(self, factor: float):
        pass

# -- Methods to work on picture --
# --- Zeichnenfunktionen ---
    
    @image_modification
    def clear(self):
        self._graphics.clear()
      
    def rect_mode(self, mode: int):
        self._graphics.rect_mode(mode)
     
    def ellipse_mode(self, mode: int):
        self._graphics.ellipse_mode(mode)

    #TODO
#     def arc
#     def circle
    
    @image_modification
    def ellipse(self,  a: int, b: int, c: int, d: int):
        self._graphics.ellipse(a,b,c,d)
        
    @image_modification
    def line(self, x1:int, y1:int,x2:int,y2:int):
        self._graphics.line(x1,y1,x2,y2)

    @image_modification
    def point(self, x:int, y:int):
        self._graphics.point(x,y)
        
    @image_modification
    def quad(self, x1:int, y1:int,x2:int,y2:int, x3:int, y3:int, x4:int, y4:int):
        self._graphics.quad(x1,y1,x2,y2,x3,y3,x4,y4)
   
    @image_modification
    def rectangle(self, a: int, b: int, c: int, d: int):
        self._graphics.rectangle(a,b,c,d)

    @image_modification
    def square(self, x:int, y:int, extend:int):
        self._graphics.square(x,y,extend)       
 
    @image_modification
    def triangle(self, x1:int, y1:int,x2:int,y2:int, x3:int, y3:int):
        self._graphics.triangle(x1,y1,x2,y2,x3,y3)
        
    @image_modification
    def text(self, s:str, x:int, y:int):
        self._graphics.text(s,x,y)

# --- Farbfestlegungen ---
    def get(self, x: int, y: int) -> color:
        """Der Farbwert an der Position x,y de"""
        raise NotImplementedError()
 
    def stroke(self, pencolor: color):
        self._graphics.stroke(pencolor)      
    
    def no_stroke(self):
        self._graphics.no_stroke()
         
    def stroke_weight(self, weight: int):
        self._graphics.stroke_weight(weight)
          
    def fill(self, fillcolor):
        self._graphics.fill(fillcolor)
          
    def no_fill(self):
        """Legt fest, dass die Formen nicht gefüllt werden sollen.
        """
        self._graphics.no_fill()
           
    @image_modification
    def background(self, argb: color):
        self._graphics.background(argb)
        
    def text_font(self, font: str):
        self._graphics.text_font(font)
        
    def text_size(self, size: int):
        self._graphics.text_size(size)
        
# --- Dateioperationen ---
    def image_mode(self):
        raise NotImplementedError
    
    def create_image(self):
        raise NotImplementedError

    def load_image(self, filename: str) -> PImage:
        """Lädt ein Bild aus dem Dateisystem

        Lädt ein Bild von einem Datentraeger und setzt Stiftfarbe und Fuellfarbe auf Standardwerte zurück.
        
        Parameters
        ----------
        filename : str
            Dateiname des Bildes
        """
        #TODO: implement some checks if file exisits
        #TODO: reset settings
        return PImage(filename=filename)
        
    def image(self, image:PImage, x:int,y:int, width: int = -1, height: int = -1):
        if width < 0: width = self.width
        if height < 0: height = self.height
        
        self._painter.begin(self._pixmap)
        self._painter.drawPixmap(QRect(x,y,width,height),image.pixmap, QRect(0,0,self.width, self.height))
        self._painter.end()
    
    def save(self, filename: str, format: Optional[str]=None, quality:int=-1):
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
        self._pixmap.save(filename, format, quality)
        
# --- Sonstiges ---   
    def delay(self, millis: int):
        """Hilfsfunktion zum Verzoegern der Ausgabe

        Parameters
        ----------
        millis : int
            Wartezeit in Millisekunden
        """

class PSurface(QMainWindow):
    """Standard Surface

    """
    
    def __init__(self, canvas: PWidget):
        super().__init__()
        #possibility for transparency in background      
        self.setAttribute(Qt.WA_TranslucentBackground) # type: ignore[attr-defined]
        
        self.setCentralWidget(canvas)
        canvas.setup()
        self.draw_loop_timer = QTimer()
        self.draw_loop_timer.setInterval(int(1000/60))
        self.draw_loop_timer.timeout.connect(canvas.draw) # type: ignore[attr-defined]
        self.draw_loop_timer.start()  
    
