import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg


class MainWindow(qtw.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hello World!')

        # Set vertical layout
        self.setLayout(qtw.QVBoxLayout())

        # Create a label
        my_label = qtw.QLabel("Hello World! What's your name")
        # Change font size of label
        my_label.setFont(qtg.QFont('Helvetica', 18))

        # Create an entry bx
        my_entry = qtw.QLineEdit()
        my_entry.setObjectName("name_field")
        my_entry.setText("Placeholder text")

        def press_it():
            # add name to label
            my_label.setText(f"Hello {my_entry.text()}")
            # clear entry box
            my_entry.setText("")

        # Create a button
        my_button = qtw.QPushButton("Press Me!")
        my_button.clicked.connect(press_it)
        self.layout().addWidget(my_label)
        self.layout().addWidget(my_entry)
        self.layout().addWidget(my_button)

        # show app
        self.show()


app = qtw.QApplication([])
mw = MainWindow()

app.exec()
