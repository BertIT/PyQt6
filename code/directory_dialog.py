from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QFileDialog,
)


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hello World!')

        # Set vertical layout
        self.setLayout(QVBoxLayout())

        # Create a label
        self.my_label = QLabel("Hello World! What's your directory?")
        self.start_button = QPushButton('Choose directory')
        self.start_button.clicked.connect(self.open_directory_dialog)

        self.layout().addWidget(self.start_button)
        self.layout().addWidget(self.my_label)
        # show app
        self.show()

    def open_directory_dialog(self):
        file_path = QFileDialog.getExistingDirectory(self, 'Choose directory')
        self.my_label.setText(file_path)


def main():
    app = QApplication([])
    mw = MainWindow()
    app.exec()


if __name__ == '__main__':
    main()
