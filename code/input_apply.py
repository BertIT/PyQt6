from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QLineEdit,
)


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hello World!')

        # Set vertical layout
        self.setLayout(QVBoxLayout())

        # Create a label
        self.my_label = QLabel('default')
        self.input_line = QLineEdit()
        self.input_line.setText('default')
        self.input_line.textChanged.connect(self.new_input_available)
        self.start_button = QPushButton('apply')
        self.start_button.setDisabled(True)
        self.start_button.clicked.connect(self.apply_input)

        self.layout().addWidget(self.start_button)
        self.layout().addWidget(self.my_label)
        self.layout().addWidget(self.input_line)
        # show app
        self.show()

    def apply_input(self):
        input_text = self.input_line.text()
        self.my_label.setText(input_text)
        self.start_button.setDisabled(True)

    def new_input_available(self):
        if self.input_line.text() != self.my_label.text():
            self.start_button.setEnabled(True)
        else:
            self.start_button.setDisabled(True)


def main():
    app = QApplication([])
    mw = MainWindow()
    app.exec()


if __name__ == '__main__':
    main()
