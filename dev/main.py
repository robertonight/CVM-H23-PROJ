import sys

from PySide6.QtCore import Slot
from PySide6.QtWidgets import (QMainWindow, QApplication, QWidget, QHBoxLayout)
from gui_left_window import Left_window
from gui_fourier import GuiFourierMain
from model import Model


class QFApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.__model = None
        self.setWindowTitle("C'est fou. Riez!")
        self.resize(1250, 900)
        self.__fourier_main = None
        self.init_gui()
        self.setStyleSheet("background-color: rgb(100,100,100);")

    def init_gui(self):
        # declarations
        self.__model = Model()
        self.__model.sim_started.connect(self.start_sim)
        self.__model.sim_updated.connect(self.update_sim)
        centralWidget = QWidget()
        layoutContainer = QHBoxLayout()
        self.__leftWindow = Left_window()
        self.__leftWindow.line_ended.connect(self.__model.receive_line)
        self.__leftWindow.undo_pushed.connect(self.__model.undo_line)
        self.__model.line_removed.connect(self.__leftWindow.undo)
        self.__leftWindow.erase_pushed.connect(self.__model.erase_drawing)
        self.__model.drawing_deleted.connect(self.erase_drawing)
        # ajout
        layoutContainer.addWidget(self.__leftWindow)
        centralWidget.setLayout(layoutContainer)
        self.__fourier_main = GuiFourierMain()
        self.__fourier_main.tick.connect(self.__model.tick)

        layoutContainer.addWidget(self.__fourier_main)

        self.setCentralWidget(centralWidget)

    @Slot()
    def start_sim(self, vectors):
        self.__fourier_main.start_sim(vectors)

    @Slot()
    def update_sim(self, vectors):
        self.__fourier_main.update_sim(vectors)

    @Slot()
    def erase_drawing(self):
        self.__leftWindow.erase_drawing()
        self.__fourier_main.erase_drawing()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QFApp()
    w.show()
    sys.exit(app.exec())
