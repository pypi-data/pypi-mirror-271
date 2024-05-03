"""TODO."""
__version__ = "0.0.3" # 2023.11
__author__ = "S. Gebert <nomisge @ live . de>"
__all__ = ['PGraphics', 'Graphics', 'Paintable']

import pysideprocessing.pconstants as pc
from pysideprocessing.color import color

from PySide6.QtGui import QPainter, QPixmap, QImage, QPen, QBrush, QPolygon, QColor, QFont
from PySide6.QtCore import Qt, QPoint
from abc import ABC, abstractmethod
from functools import wraps, singledispatchmethod

def shape_painter(method):
    @wraps(method)
    def _impl(self,*method_args, **method_kwargs):
        #TODO: !Speedup maybe by calling begin / end less often?
        self._painter.begin(self._paint_device.get_paint_device()) # pylint: disable=protected-access
        self._painter.setPen(self._pen if self._stroke else Qt.NoPen) # pylint: disable=protected-access # type: ignore[attr-defined]
        self._painter.setBrush(self._brush if self._fill else Qt.NoBrush) # pylint: disable=protected-access # type: ignore[attr-defined]
        self._text_font.setPointSize(self._text_size) # pylint: disable=protected-access
        self._painter.setFont(self._text_font) # pylint: disable=protected-access
        method(self,*method_args, **method_kwargs)
        self._painter.end() # pylint: disable=protected-access
    return _impl


class Paintable(ABC):
    @abstractmethod
    def get_paint_device(self) -> QPixmap|QImage:
        raise NotImplementedError

class Graphics(ABC):
# -- MODE Settings --
    @abstractmethod
    def rect_mode(self, mode: int):
        """Ändert den Koordinaten-Modus beim Zeichnen von Rechtecken.
        
        Ändert die Position, von der aus Rechtecke gezeichnet werden, indem es die Art und Weise aendert, wie Parameter, die an rect() uebergeben werden, interpretiert werden.
        Der Standardmodus ist rectMode(Bild.CORNER), der die ersten beiden Parameter von rect() als die linke obere Ecke der Form interpretiert, 
        waehrend der dritte und vierte Parameter seine Breite und Hoehe sind.
        rectMode(Bild.CORNERS) interpretiert die ersten beiden Parameter von rect() als die Position einer Ecke 
        und die dritten und vierten Parameter als die Position der gegenueberliegenden Ecke.
        rectMode(Bild.CENTER) interpretiert die ersten beiden Parameter von rect() als Mittelpunkt der Form, 
        waehrend der dritte und vierte Parameter seine Breite und Hoehe sind.
        rectMode(RADIUS) verwendet auch die ersten beiden Parameter von rect() als Mittelpunkt der Form, 
        verwendet aber den dritten und vierten Parameter, um die Haelfte der Breite und Hoehe der Formen festzulegen.

        Parameters
        ----------
        mode : int
            Modus der Koordinateninterpretation (CORNER, CORNERS, CENTER oder RADIUS)
        """
    @abstractmethod
    def ellipse_mode(self, mode: int):
        """Ändert den Koordinaten-Modus beim Zeichnen von Kreisen/Ellipsen.

        Ändert die Position, von der aus Kreise/Ellipsen gezeichnet werden, indem es die Art und Weise aendert, wie Parameter, die an ellipse() uebergeben werden, interpretiert werden.
        Der Standardmodus ist ellipseMode(Bild.CENTER), der die ersten beiden Parameter von ellipse() als Mittelpunkt der Form interpretiert, 
        waehrend der dritte und vierte Parameter seine Breite und Hoehe sind.
        ellipseMode(Bild.CORNER) interpretiert die ersten beiden Parameter von ellipse() als die Position einer Ecke 
        und die dritten und vierten Parameter als Breite und Hoehe der Form.
        ellipseMode(Bild.CORNERS) interpretiert die ersten beiden Parameter von ellipse() als die Position einer Ecke 
        und die dritten und vierten Parameter als die Position der gegenueberliegenden Ecke.
        ellipseMode(RADIUS) verwendet auch die ersten beiden Parameter von ellipse() als Mittelpunkt der Form, 
        verwendet aber den dritten und vierten Parameter, um die Haelfte der Breite und Hoehe der Formen festzulegen.
        Parameters
        ----------
        mode : int
            Modus der Koordinateninterpretation (CORNER, CORNERS, CENTER oder RADIUS)
        """
        
# -- Draw settings
    @abstractmethod
    def stroke(self, pencolor: color):
        """Legt die Farbe fest, mit der Linien und Raender um Formen gezeichnet werden.
        """
        
    @abstractmethod        
    def no_stroke(self):
        """Legt fest, dass keine Linien oder Raender um Formen gezeichnet werden soll.
        """
        
    @abstractmethod        
    def stroke_weight(self, weight: int):
        """Legt die Breite des Strichs fuer Linien, Punkte und den Rand um Formen fest.

        Alle Breiten werden in Pixeleinheiten angegeben.
        
        Parameters
        ----------
        weight : float
            Breite in Pixel
        """
        
    @abstractmethod    
    def fill(self, fillcolor: color):
        """Legt die Farbe fest, mit der Formen gefüllt werden.

        """       

    @abstractmethod
    def no_fill(self):
        """Legt fest, dass die Formen nicht gefüllt werden sollen.
        """

    @abstractmethod
    def text_font(self, font: str):
        """Legt die Schriftart fest, in der Text gedruckt wird.
        """
 
    @abstractmethod
    def text_size(self, size: int):
        """Legt die Schriftgröße fest, in der Text gedruckt wird.
        """
        
# -- Background operations
    @abstractmethod
    def background(self, backgroundcolor: color):
        """Sets the color used for the background of the Processing window.
            
        The default background is light gray. This function is
        typically used within **draw()** to clear the display window at the
        beginning of each frame, but it can be used inside **setup()** to set the
        background on the first frame of animation or if the background need only be
        set once.
        
        An image can also be used as the background for a sketch, although the
        image's width and height must match that of the sketch window. Images used
        with **background()** will ignore the current **tint()** setting. To
        resize an image to the size of the sketch window, use image.resize(width,
        height).

        It is not possible to use the transparency **alpha** parameter with
        background colors on the main drawing surface. It can only be used along with
        a **PGraphics** object and **createGraphics()**.
       
       
        Advanced
        --------
        Clear the background with a color that includes an alpha value. This can only
        be used with objects created by createGraphics(), because the main drawing
        surface cannot be set transparent.
        
        It might be tempting to use this function to partially clear the screen on
        each frame, however that's not how this function works. When calling
        background(), the pixels will be replaced with pixels that have that level of
        transparency. To do a semi-transparent overlay, use fill() with alpha and
        draw a rectangle.
        
        Parameters
        ----------
        backgroundcolor:
            argb value of the color to be set as background color.
            If None, background is filled with last background set.
        """

    @abstractmethod
    def clear(self):
        """Löscht den Inhalt des Bildes.

        Der Hintergrund wird mir der Hintergrundfarbe neu gefüllt.
        """

# -- Shapes
    #TODO
#     def arc
#     def circle
    @abstractmethod
    def ellipse(self,  a: int, b: int, c: int, d: int):
        """Zeichnet eine Ellipse/Kreis auf das Bild.

        Standardmaessig legen die ersten beiden Parameter die Position des Mittelpunkts fest, der dritte die Breite und der vierte die Hoehe. 
        Die Art und Weise, wie diese Parameter interpretiert werden, kann jedoch mit der Funktion {@link #ellipseMode(int) ellipseMode()} geaendert werden.
        Durch den Befehl {@link #fill(int,int,int) fill()} /{@link #noFill() noFill()} kann die Fuellfarbe des Rechtecks gewaehlt werden, durch {@link #stroke(int, int, int) stroke()}/{@link #noStroke() noStroke()}  die Rahmenfarbe.
     
        Parameters
        ----------
        a:int
            meist die x-Koordinate des Mittelpunkts (kann durch ellipseMode() geaendert werden).
        b:int
            meist die y-Koordinate des Mittelpunkts (kann durch ellipseMode() geaendert werden).
        c:int
            meist die Breite des Rechtecks (kann durch ellipseMode() geaendert werden).
        d:int
            meist die Hoehe des Rechtecks (kann durch ellipseMode() geaendert werden).
        """

    @abstractmethod 
    def line(self, x1:int, y1:int,x2:int,y2:int):
        """Zeichnet eine Linie (einen direkten Weg zwischen zwei Punkten) auf den Bildschirm.
        
        Um eine Linie einzufaerben, verwenden Sie die :meth:`~stroke` Funktion. Eine Zeile
        kann nicht gefuellt werden, daher hat die Funktion :meth:`~fill` keinen Einfluss auf die
        Farbe einer Zeile. Linien werden standardmäßig mit einer Breite von einem Pixel
        gezeichnet, dies kann jedoch mit der Funktion :meth:`~strokeWeight` geändert werden.
        
        Parameters
        ----------
        x1:
            x-Koordinate des 1. Punktes
        y1:
            y-Koordinate des 1. Punktes
        x2:
            x-Koordinate des 2. Punktes
        y2:
            y-Koordinate des 2. Punktes
        """
    
    @abstractmethod
    def point(self, x:int, y:int):
        """Zeichnet einen Punkt, d.h. einen Kreis in der Dimension eines Pixels. 
        
        Der erste Parameter ist der x-Wert fuer den Punkt, der zweite Wert ist der y-Wert fuer den Punkt.
        
        Parameters
        ----------
        x:
            x-Koordinate des Punktes
        y:
            y-Koordinate des Punktes
        """
        
    @abstractmethod
    def quad(self, x1:int, y1:int,x2:int,y2:int, x3:int, y3:int, x4:int, y4:int):
        """Zeichnet ein Viereck auf das Bild. 
        
        Ein Viereck ist ein vierseitiges Polygon. Es ist aehnlich wie ein Rechteck, aber die Winkel zwischen seinen Kanten 
        sind nicht auf neunzig Grad beschraenkt. Das erste Paar von Parametern (x1,y1) setzt den ersten Scheitelpunkt und die nachfolgenden 
        Paare sollten im Uhrzeigersinn oder gegen den Uhrzeigersinn um die definierte Form herum verlaufen. 
        Durch den Befehl {@link #fill(int,int,int) fill()} /{@link #noFill() noFill()} kann die Fuellfarbe des Rechtecks gewaehlt werden, durch {@link #stroke(int, int, int) stroke()}/{@link #noStroke() noStroke()}  die Rahmenfarbe.
        
        Parameters
        ----------
        x1:int
            meist die x-Koordinate des 1. Punkts.
        y1:int
            meist die y-Koordinate des 1. Punkts.
        x2:int
            meist die x-Koordinate des 2. Punkts.
        y2:int
            meist die y-Koordinate des 2. Punkts.
        x3:int
            meist die x-Koordinate des 3. Punkts.
        y3:int
            meist die y-Koordinate des 3. Punkts.
        """
        
    @abstractmethod
    def rectangle(self, a: int, b: int, c: int, d: int):
        """Zeichnet ein Rechteck auf das Bild.
        
        Standardmaessig legen die ersten beiden Parameter die Position der linken oberen Ecke fest, der dritte die Breite und der vierte die Hoehe.
        Die Art und Weise, wie diese Parameter interpretiert werden, kann jedoch mit der Funktion {@link #rectMode(int) rectMode()} geaendert werden.
        Durch den Befehl {@link #fill(int,int,int) fill()} /{@link #noFill() noFill()}  kann die Fuellfarbe des Rechtecks gewaehlt werden, durch {@link #stroke(int, int, int) stroke()}/{@link #noStroke() noStroke()}  die Rahmenfarbe.
        
        Parameters
        ----------
        a: int
            meist die x-Koordinate der linken oberen Ecke (kann durch rectMode() geaendert werden).
        b: int
            meist die y-Koordinate der linken oberen Ecke (kann durch rectMode() geaendert werden).
        c: int
            meist die Breite des Rechtecks (kann durch rectMode() geaendert werden).
        d: int
            meist die Hoehe des Rechtecks (kann durch rectMode() geaendert werden).
        """

    @abstractmethod
    def square(self, x:int, y:int, extend:int):
        """Zeichnet ein Quadrat auf das Bild.

        Parameters
        ----------
        x : int
            meist die x-Koordinate der linken oberen Ecke (kann durch rectMode() geaendert werden).
        y : int
            meist die y-Koordinate der linken oberen Ecke (kann durch rectMode() geaendert werden).
        extend: int
            meist die Länge des Quadrats
        """
        
    @abstractmethod
    def triangle(self, x1:int, y1:int,x2:int,y2:int, x3:int, y3:int):
        """Zeichnet ein Dreieck auf das Bild.
        
        Ein Dreieck ist eine Ebene, die durch die Verbindung von drei Punkten entsteht. Die ersten beiden Argumente spezifizieren den
        ersten Punkt, die mittleren beiden Argumente spezifizieren den zweiten Punkt und die letzten beiden Argumente spezifizieren den dritten Punkt.
        Durch den Befehl `fill` /`noFill` kann die Fuellfarbe des Rechtecks gewaehlt werden, durch `stroke`/`noStroke` die Rahmenfarbe.
        
        Parameters
        ----------
        x1 : int
            meist die x-Koordinate des 1. Punkts.
        y1 : int
            meist die y-Koordinate des 1. Punkts.
        x2 : int
            meist die x-Koordinate des 2. Punkts.
        y2 : int
            meist die y-Koordinate des 2. Punkts.
        x3 : int
            meist die x-Koordinate des 3. Punkts.
        y3 : int
            meist die y-Koordinate des 3. Punkts.
        """
        
    @abstractmethod        
    def text(self, s:str, x:int, y:int):        
        """Gibt einen Text an den gegebenen Koordinaten aus
        
        Zur Ausgabe des Textes wird der ausgewaehlte Font verwendet. Dieser muss vorher mit {@link #textFont(Font) textFont() } festgelegt.
        
        Parameters
        ----------
        s : str
            Text, der angezeigt werden soll
        x : int
            x-Koordinate des Textanfangs
        y : int
            y-Koordinate der Grundlinie des Textes.
        """

class PGraphics(Graphics):
    _painter: QPainter
    _paint_device: Paintable
    
    _rect_mode: int
    _ellipse_mode: int
    
    _background: int
    
    _stroke: bool
    _pen: QPen
    _fill: bool
    _brush: QBrush
     
    _text_font: QFont
    _text_size: int
    _text_align: int
    
    def __init__(self, paint_device: Paintable):
#         super().__init__()
        self._painter = QPainter()
        self._paint_device = paint_device
        
        self._background = 0xffd3d3d3

        self.clear()
        self._stroke = True
        self._pen = QPen()
        self._pen.setWidth(4)
        self._pen.setColor(QColor.fromRgba(int(color("black"))))
        
        self._fill = True
        self._brush = QBrush(Qt.SolidPattern) # type: ignore[attr-defined]
        self._brush.setColor(QColor.fromRgba(int(color("white"))))

        self._text_font = QFont()
        self._text_font.setFamily('Times')
        self._text_font.setBold(False)
        self._text_size =12
        
        self._rect_mode = pc.CORNER
        self._ellipse_mode = pc.CENTER
                
    @property
    def painter(self) -> QPainter:
        return self._painter
#     @property
#     def pen(self) -> QPen:
#         return self._pen

    
# -- MODE Settings --
    
    def rect_mode(self, mode: int):
        self._rect_mode = mode
   
    def ellipse_mode(self, mode: int):
        self._ellipse_mode = mode
        
# -- Draw settings
    
    def stroke(self, pencolor: color):
        self._stroke = True
        self._pen.setColor(QColor.fromRgba(int(pencolor)))
  
    def no_stroke(self):
        self._stroke = False
  
    def stroke_weight(self, weight: int):
        self._pen.setWidth(weight)

    def fill(self, fillcolor: color):
        self._fill = True
        self._brush.setColor(QColor.fromRgba(int(fillcolor)))

    def no_fill(self):
#         self._brush = 
        self._fill = False

    def text_font(self, font: str):
        new_font = QFont()
        new_font.setFamily('Times')
        new_font.setBold(False)
        self._text_font = new_font
        #TODO: create font by string or some class?

    def text_size(self, size: int):
        self._text_size = size

# -- Background operations
    
    def clear(self):
        self._paint_device.get_paint_device().fill(QColor.fromRgba(self._background))
    
    @singledispatchmethod
    def background(self, backgroundcolor: color): # type: ignore[override]
        #TODO: allow images or numbers etc. instead of argb int    
        self._background = int(backgroundcolor)
        self.clear()
    @background.register
    def _(self, backgroundcolor: int):
        self._background = backgroundcolor
        self.clear()

# -- Shapes
    #TODO
#     def arc
#     def circle
    @shape_painter
    def ellipse(self, a: int, b: int, c: int, d: int):
        self._painter.drawEllipse(a,b,c,d)
        
    @shape_painter
    def line(self, x1:int, y1:int, x2:int, y2:int):
        self._painter.drawLine(x1,y1,x2,y2)
    
    @shape_painter
    def point(self, x:int, y:int):
        self._painter.drawPoint(x,y)
        
    @shape_painter    
    def quad(self, x1:int, y1:int,x2:int,y2:int, x3:int, y3:int, x4:int, y4:int):
        p = QPolygon.fromList([QPoint(x1,y1), QPoint(x2,y2), QPoint(x3,y3), QPoint(x4,y4)])
        self._painter.drawPolygon(p)
        
    @shape_painter
    def rectangle(self, a: int, b: int, c: int, d: int):
        self._painter.drawRect(a,b,c,d)
      
    @shape_painter
    def square(self, x:int, y:int, extend:int):
        self._painter.drawRect(x,y,extend,extend)
    
    @shape_painter
    def triangle(self, x1:int, y1:int,x2:int,y2:int, x3:int, y3:int):
        p = QPolygon.fromList([QPoint(x1,y1), QPoint(x2,y2), QPoint(x3,y3)])
#         p = p << QPoint(x1,y1) << QPoint(x2,y2) << QPoint(x3,y3)
        self._painter.drawPolygon(p)

    @shape_painter
    def text(self, s:str, x:int, y:int):
        self._painter.drawText(x,y, s)
        #TODO: handle different inputs, e.g. with more parameters...

