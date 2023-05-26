import os
import sys
from functools import partial

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
        self.cursorMove.connect(self.handle_cursor_move)
        self.timer = QTimer(self)
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.poll_cursor)
        self.timer.start()
        self.cursor = None
        self.color = None
        self.selected_color = None
        self.button_list = [
            self.css_selected_button,
            self.hex_selected_button,
            self.css_hover_button,
            self.hex_hover_button,
        ]
        for button in self.button_list:
            button.clicked.connect(partial(self.button_clicked, button))

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

    def button_clicked(self, btn):
        clipboard = QApplication.clipboard()
        match btn.objectName():
            case "css_hover_button":
                clipboard.setText(f"color: rgb({self.color.red()},{self.color.green()},{self.color.blue()});")
            case "hex_hover_button":
                clipboard.setText(f"#{self.color.red():02X}{self.color.green():02X}{self.color.blue():02X}")
            case "css_selected_button":
                clipboard.setText(
                    f"color: rgb({self.selected_color.red()},{self.selected_color.green()},{self.selected_color.blue()});",
                )
            case "hex_selected_button":
                clipboard.setText(
                    f"#{self.selected_color.red():02X}{self.selected_color.green():02X}{self.selected_color.blue():02X}",
                )

    def handle_cursor_move(self, pos):
        self.main.hover_input.setText(f"R:{self.color.red()},G:{self.color.green()},B:{self.color.blue()}")
        self.main.hover_box.setStyleSheet(
            f"background: rgb({self.color.red()},{self.color.green()},{self.color.blue()});",
        )

    def selectColor(self):
        self.selected_color = self.color
        self.main.selected_input.setText(f"R:{self.color.red()},G:{self.color.green()},B:{self.color.blue()}")
        self.main.selected_box.setStyleSheet(
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
