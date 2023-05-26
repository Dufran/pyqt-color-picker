import os
import sys

from PyQt6 import uic
from PyQt6.QtCore import QEvent, QObject, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QColor, QCursor, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow
from qt_material import apply_stylesheet


class GlobalEventFilter(QObject):
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.WindowDeactivate:
            window.selectColor()
            return True
        return False


class ColorPicker(QMainWindow):
    # * Signal to handle cursor movement outside window
    cursorMove = pyqtSignal(object)

    def __init__(self):
        super().__init__()

        self.main = uic.loadUi(os.path.join(os.path.dirname(__file__), "assets", "main.ui"), self)
        self.cursorMove.connect(self.handleCursorMove)
        self.timer = QTimer(self)
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.poll_cursor)
        self.timer.start()
        self.cursor = None
        self.color = None
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "assets", "icon.png")))

    def poll_cursor(self):
        screen = QApplication.primaryScreen()
        cursor = QCursor()
        position = cursor.pos()
        x, y = position.x(), position.y()
        image = screen.grabWindow(0, x, y, 1, 1).toImage()
        color = QColor(image.pixel(0, 0))

        if position != self.cursor:
            self.cursor = position
            self.color = color
            self.cursorMove.emit(position)

    def handleCursorMove(self, pos):
        self.main.lineEdit.setText(f"R:{self.color.red()},G:{self.color.green()},B:{self.color.blue()}")
        self.main.graphicsView_2.setStyleSheet(
            f"background: rgb({self.color.red()},{self.color.green()},{self.color.blue()});",
        )

    def selectColor(self):
        self.main.lineEdit_2.setText(f"R:{self.color.red()},G:{self.color.green()},B:{self.color.blue()}")
        self.main.graphicsView.setStyleSheet(
            f"background: rgb({self.color.red()},{self.color.green()},{self.color.blue()});",
        )


if __name__ == "__main__":
    # Create the application object
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme="dark_amber.xml")
    _filter = GlobalEventFilter()
    app.installEventFilter(_filter)
    # Create the main window
    window = ColorPicker()
    window.main.show()

    # Run the event loop
    sys.exit(app.exec())
