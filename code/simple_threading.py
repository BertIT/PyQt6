import time

import PyQt6.QtWidgets as qtw
from PyQt6 import QtCore


class Function(QtCore.QObject):

    log_signal = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

    def print_text(self, string):
        self.log_signal.emit(string)

    def run_function(self):
        self.print_text('Program started')
        time.sleep(1)
        self.print_text('do something ...')
        time.sleep(3)
        self.print_text('Program finished')
        self.finished.emit()


class MainWindow(qtw.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hello World!')

        # Set vertical layout
        self.setLayout(qtw.QVBoxLayout())
        self.func = Function()

        # Create a label
        self.my_label = qtw.QLabel("Hello World! What's your name")
        self.start_button = qtw.QPushButton('Start me!')
        self.start_button.clicked.connect(self.run_start_button)

        self.layout().addWidget(self.start_button)
        self.layout().addWidget(self.my_label)
        # show app
        self.show()

    def run_start_button(self):

        self.func.log_signal.connect(self.set_log_text)

        self.func_thread = QtCore.QThread(self)
        self.func.moveToThread(self.func_thread)
        self.func_thread.started.connect(self.func.run_function)
        self.func.finished.connect(self.func_thread.quit)
        self.func_thread.start()

    def set_log_text(self, log_text):
        self.my_label.setText(log_text)


app = qtw.QApplication([])
mw = MainWindow()

app.exec()
