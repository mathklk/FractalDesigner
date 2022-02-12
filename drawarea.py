from PyQt5.QtWidgets import *
from PyQt5.QtGui import *#QRgba64, QImage, QPainter, QPaintEvent, QResizeEvent
from PyQt5.QtCore import *#QRect, Qt, QSize



class DrawArea(QWidget):
    def __init__(self):
        super(DrawArea, self).__init__()
        self.setAttribute(Qt.WA_AcceptTouchEvents)
        self.setAttribute(Qt.WA_StaticContents)
        self.image: QImage = QImage(16, 9, QImage.Format_RGB16)
        self.scaleFactor = 1
        self.modified: bool = False

        self.clearImage()

    # Static methods

    @staticmethod
    def backgroundColor() -> QColor:
        return QColor(255, 255, 255)

    @staticmethod
    def primaryColor() -> QColor:
        return QColor(0, 0, 0)

    @staticmethod
    def secondaryColor() -> QColor:
        return QColor(255, 0, 0)

    # Public methods

    def clearImage(self):
        self.image.fill(self.backgroundColor())
        self.modified = True
        self.update()

    """
    def resizeImage(self, image: QImage, newSize: QSize):
        if (image.size() == newSize):
            return

        newImage: QImage = QImage(newSize, QImage.Format_RGB16)
        newImage.fill(self.backgroundColor())
        painter: QPainter = QPainter(newImage)
        painter.drawImage(QPoint(0, 0), image)
        painter.end()
        self.image = newImage
    """

    # Events

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        rect: QRect = event.rect()

        #relevantImage = self.image.copy(self._relevantRect())\
        #    .scaled(rect.width(), rect.height(), aspectRatioMode=Qt.KeepAspectRatio)

        self.scaleFactor = min(self.height() / self.image.height(), self.width() / self.image.width())
        scaledSize: QSize = self.image.size() * self.scaleFactor
        scaledImage = self.image.scaled(scaledSize, aspectRatioMode=Qt.KeepAspectRatio)

        painter.drawImage(rect.topLeft(), scaledImage, rect)

    def resizeEvent(self, event: QResizeEvent):
        #if (self.width() > self.image.width()) or (self.height() > self.image.height()):
        #    newWidth: int  = max(self.width()  + 128, self.image.width())
        #    newHeight: int = max(self.height() + 128, self.image.height())
        #    self.resizeImage(self.image, QSize(newWidth, newHeight))
        #    self.update()
        super().resizeEvent(event)

    def event(self, event: QEvent) -> bool:
        if type(event) == QMouseEvent:
            self._drawMethod(event)
        else:
            #print("Other event", type(event))
            return super(DrawArea, self).event(event)
        return True

    # Private Methods


    def _drawMethod(self, event: QMouseEvent):
        painter: QPainter = QPainter(self.image)
        clickedMouseButtons = event.buttons()
        point: QPoint = QPoint(event.x(), event.y())

        guiRect = QRect(QPoint(0, 0), self.image.size() * self.scaleFactor)
        if not guiRect.contains(point, proper=True):
            print("Klick war außerhalb der Darstellung, abort.")
            return

        midOffset = QPoint(self.scaleFactor // 2, self.scaleFactor // 2)
        projectedPoint = (point - midOffset) / self.scaleFactor

        print("Punkt", point, "wurde auf", projectedPoint, "projeziert. (Faktor", self.scaleFactor, ")")
        if clickedMouseButtons & Qt.LeftButton:
            painter.setPen(self.primaryColor())
            painter.drawPoint(projectedPoint)
        elif clickedMouseButtons & Qt.RightButton:
            painter.setPen(self.backgroundColor())
            painter.drawPoint(projectedPoint)
        elif clickedMouseButtons & Qt.MiddleButton:
            painter.setPen(self.secondaryColor())
            painter.drawPoint(projectedPoint)
        #self.update(QRect(point, QPoint(1, 1)))
        self.update()
        painter.end()

    def _relevantRect(self) -> QRect:
        top = 0
        bot = self.image.height()
        left = 0
        right = self.image.width()

        for y in range(self.image.height() - 1):
            isEmpty = True
            for x in range(self.image.width()):
                #print("Now checking",x,y,self.image.pixelColor(x, y))
                if self.image.pixelColor(x, y) != self.backgroundColor():
                    isEmpty = False
                    break

            if isEmpty:
                top = y
            else:
                break

        for y in range(self.image.height() - 1, 0, -1):
            isEmpty = True
            for x in range(self.image.width()):
                #print("2Now checking", x, y, self.image.pixelColor(x, y))
                if self.image.pixelColor(x, y) != self.backgroundColor():
                    isEmpty = False
                    break

            if isEmpty:
                bot = y
            else:
                break

        for x in range(self.image.width() - 1):
            isEmpty = True
            for y in range(self.image.height()):
                #print("Now checking",x,y,self.image.pixelColor(x, y))
                if self.image.pixelColor(x, y) != self.backgroundColor():
                    isEmpty = False
                    break

            if isEmpty:
                left = x
            else:
                break

        for x in range(self.image.width() - 1, 0, -1):
            isEmpty = True
            for y in range(self.image.height()):
                #print("2Now checking", x, y, self.image.pixelColor(x, y))
                if self.image.pixelColor(x, y) != self.backgroundColor():
                    isEmpty = False
                    break

            if isEmpty:
                right = x
            else:
                break

        return QRect(QPoint(left, top), QPoint(right, bot))

