import time

import PyQt6.QtWidgets as qtw
from PyQt6 import QtCore
from PyQt6.QtGui import QColor


class Function(QtCore.QObject):
    log_signal = QtCore.pyqtSignal(str)
    color_signal = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.log_text = ''

    def print_text(self, string: str, color: str = 'black') -> None:
        self.color_signal.emit(color)
        self.log_signal.emit(string)

    def run_function(self) -> None:
        self.print_text('Program started', 'green')
        time.sleep(1)
        self.print_text('do something ...', 'red')
        time.sleep(3)
        for i in range(20):
            self.print_text(f'... task {i}', 'blue')
            time.sleep(0.1)
        self.print_text('Program finished', 'green')
        self.finished.emit()


class MainWindow(qtw.QWidget):
    colors = {
        'black': QColor(0, 0, 0),
        'green': QColor(0, 255, 0),
        'red': QColor(255, 0, 0),
        'blue': QColor(0, 0, 255),
    }

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hello World!')

        # Create a label
        self.log_out = qtw.QTextEdit("Hello World! What's your name")
        self.log_out.setReadOnly(True)
        self.log_out.setStyleSheet("background-color: rgb(150, 150, 150);")
        self.log_out_sb = self.log_out.verticalScrollBar()

        self.start_button = qtw.QPushButton('Start me!')
        self.start_button.clicked.connect(self.run_start_button)

        # Set vertical layout
        self.setLayout(qtw.QVBoxLayout())
        self.layout().addWidget(self.start_button)
        self.layout().addWidget(self.log_out)

        self.func_thread = None
        self.func = None

        # show app
        self.show()

    def run_start_button(self) -> None:
        self.func_thread = QtCore.QThread(self)
        self.func = Function()

        self.func.moveToThread(self.func_thread)

        self.func_thread.started.connect(self.func.run_function)
        self.func.finished.connect(self.func_thread.quit)
        self.func.finished.connect(self.func.deleteLater)
        self.func_thread.finished.connect(self.func_thread.deleteLater)
        self.func.color_signal.connect(self.set_log_color)
        self.func.log_signal.connect(self.set_log_text)
        self.log_out.clear()

        self.func_thread.start()

    def set_log_color(self, color: str) -> None:
        self.log_out.setTextColor(self.colors[color])

    def set_log_text(self, log_text: str) -> None:
        self.log_out.append(log_text)
        self.log_out_sb.setValue(self.log_out_sb.maximum())


def main() -> None:
    app = qtw.QApplication([])
    mw = MainWindow()
    mw.resize(500, 300)
    app.exec()


if __name__ == '__main__':
    main()