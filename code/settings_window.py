import time
import random

import PyQt6.QtWidgets as qtw
from PyQt6 import QtCore
from PyQt6.QtGui import QColor
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure
import pandas as pd


RED = QColor(255, 0, 0)
GREEN = QColor(0, 255, 0)
BLUE = QColor(0, 0, 255)
BLACK = QColor(0, 0, 0)


class Function(QtCore.QObject):
    log_signal = QtCore.pyqtSignal(str)
    color_signal = QtCore.pyqtSignal(QColor)
    df_signal = QtCore.pyqtSignal(pd.DataFrame)
    finished = QtCore.pyqtSignal()

    def __init__(self, factor_value):
        super().__init__()
        self.log_text = ''
        self.factor = factor_value

    def print_text(self, string: str, color: QColor = BLACK) -> None:
        self.color_signal.emit(color)
        self.log_signal.emit(str(string))

    def run_function(self) -> None:

        self.print_text('Program started', GREEN)
        time.sleep(1)
        self.print_text('do something ...', RED)
        time.sleep(3)
        cats = [[i * self.factor for i in random.choices(range(10), k=3)]
                for _ in range(3)]
        self.print_text(f'Function factor_value: {self.factor}')
        self.print_text(type(cats))
        for cat in cats:
            self.print_text(cat)

        ampel_df = pd.DataFrame(
            [['Cat 1'] + cats[0],
             ['Cat 2'] + cats[1],
             ['Cat 3'] + cats[2]],
            columns=['category', 'green', 'yellow', 'red']
        )
        self.df_signal.emit(ampel_df)

        for i in range(20):
            self.print_text(f'... task {i}', BLUE)
            time.sleep(0.1)
        self.print_text('Program finished', GREEN)
        self.finished.emit()


class SettingsWindow(qtw.QWidget):
    factor_signal = QtCore.pyqtSignal(float)
    close_signal = QtCore.pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.label = qtw.QLabel("Settings")
        self.input_field = qtw.QLineEdit("1")
        # self.input_field.setFixedWidth(30)
        self.input_field.setFixedSize(50, 20)
        self.input_field.returnPressed.connect(self.ok)
        self.ok_button = qtw.QPushButton('OK')
        self.ok_button.clicked.connect(self.ok)
        self.ok_button.setAutoDefault(False)
        self.ok_button.setDefault(True)

        layout = qtw.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)

    def ok(self):
        try:
            factor = float(self.input_field.text())
            print(factor)
            print(type(factor))
            self.factor_signal.emit(factor)
            self.close_signal.emit(True)

        except ValueError:
            self.label.setText("Input is no float format (e.g. '3.67')")


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(
            figsize=(width, height),
            dpi=dpi,
            layout='tight',
            facecolor=(0.6, 0.6, 0.6),
        )
        self.axes = fig.add_subplot(1, 1, 1)
        super(MplCanvas, self).__init__(fig)


class MainWindow(qtw.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hello World!')
        self.w = None
        # Create a label
        self.log_out = qtw.QTextEdit("Hello World! What's your name")
        self.log_out.setReadOnly(True)
        self.log_out.setStyleSheet("background-color: rgb(150, 150, 150);")
        self.log_out_sb = self.log_out.verticalScrollBar()

        self.start_button = qtw.QPushButton('Start me!')
        self.start_button.clicked.connect(self.run_start_button)

        self.settings_button = qtw.QPushButton('Settings')
        self.settings_button.clicked.connect(self.open_settings)

        # plot
        self.df_2_plot = pd.DataFrame(
            [['Cat 1', 1, 1, 1],
             ['Cat 2', 1, 1, 1],
             ['Cat 3', 1, 1, 1]],
            columns=['category', 'green', 'yellow', 'red'],
        )
        self.factor_value = 1
        self.sc = None
        self.ax = None
        self.setup_chart_canvas()
        # self.plot_df()

        self.toolbar = NavigationToolbar(self.sc, self)

        # Set vertical layout
        self.setLayout(qtw.QVBoxLayout())
        self.layout().addWidget(self.start_button)
        self.layout().addWidget(self.settings_button)
        self.layout().addWidget(self.log_out)
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.sc)

        self.func_thread = None
        self.func = None

        # show app
        self.show()

    def setup_chart_canvas(self):
        self.sc = MplCanvas(self)
        self.ax = self.sc.axes
        self.ax.set_facecolor((0.6, 0.6, 0.6))

    def plot_df(self):
        self.df_2_plot.plot(
            x='category',
            kind='bar',
            stacked=False,
            title='Ampelskala',
            ax=self.ax,
            color=[(0.3, 0.7, 0), (0.9, 0.8, 0), (0.8, 0, 0)],
            legend=False,
        )

    def open_settings(self, checked):
        if self.w is None:
            self.w = SettingsWindow()
            self.w.factor_signal.connect(self.set_factor_value)
            self.w.close_signal.connect(self.close_settings)
        self.w.show()

    def close_settings(self, close: bool) -> None:
        if self.w and close:
            self.w.close()

    def set_factor_value(self, val: float) -> None:
        print(f'received: {val}')
        self.factor_value = val

    def run_start_button(self) -> None:

        self.start_button.setDisabled(True)
        self.func_thread = QtCore.QThread(self)
        print(f'send to functions: {self.factor_value}')
        self.func = Function(self.factor_value)

        self.func.moveToThread(self.func_thread)

        self.func_thread.started.connect(self.func.run_function)
        self.func.finished.connect(self.func_thread.quit)
        self.func.finished.connect(self.func.deleteLater)
        self.func.finished.connect(self.set_start_button_enabled)
        self.func_thread.finished.connect(self.func_thread.deleteLater)
        self.func.color_signal.connect(self.set_log_color)
        self.func.log_signal.connect(self.set_log_text)
        self.func.df_signal.connect(self.refresh_plot_df)
        self.log_out.clear()

        self.func_thread.start()

    def set_start_button_enabled(self):
        self.start_button.setEnabled(True)

    def set_log_color(self, color: QColor) -> None:
        self.log_out.setTextColor(color)

    def set_log_text(self, log_text: str) -> None:
        self.log_out.append(log_text)
        self.log_out_sb.setValue(self.log_out_sb.maximum())

    def refresh_plot_df(self, df: pd.DataFrame):
        print(df)
        print(type(df))
        self.df_2_plot = df
        self.sc.axes.cla()
        self.plot_df()
        self.sc.draw()


def main() -> None:
    app = qtw.QApplication([])
    mw = MainWindow()
    mw.resize(500, 300)
    app.exec()


if __name__ == '__main__':
    main()
