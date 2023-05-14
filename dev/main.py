import sys

from PySide6.QtCore import Slot
from PySide6.QtWidgets import (QMainWindow, QApplication, QWidget, QHBoxLayout)
from gui_left_window import Left_window
from gui_fourier import GuiFourierMain
from model import Model
from gui_feed import GuiFeedMain

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
        centralWidget = self.change_to_fourier_windows()

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

    @Slot()
    def change_to_feed(self):
        self.__fourier_main.stop_sim()
        self.__model.stop_sim()
        new_central_widget = GuiFeedMain()
        new_central_widget.return_pushed.connect(self.quit_feed)
        self.setCentralWidget(new_central_widget)

    @Slot()
    def quit_feed(self):
        new_central_widget = self.change_to_fourier_windows()
        self.setCentralWidget(new_central_widget)

    def change_to_fourier_windows(self):
        centralWidget = QWidget()
        layoutContainer = QHBoxLayout()
        self.__leftWindow = Left_window()
        self.__leftWindow.line_ended.connect(self.__model.receive_line)
        self.__leftWindow.undo_pushed.connect(self.__model.undo_line)
        self.__model.line_removed.connect(self.__leftWindow.undo)
        self.__leftWindow.erase_pushed.connect(self.__model.erase_drawing)
        self.__model.drawing_deleted.connect(self.erase_drawing)
        self.__leftWindow.drawing_saved.connect(self.__model.save_drawing)
        self.__leftWindow.cliked_feed.connect(self.change_to_feed)
        # ajout
        layoutContainer.addWidget(self.__leftWindow)
        centralWidget.setLayout(layoutContainer)
        self.__fourier_main = GuiFourierMain()
        self.__fourier_main.tick.connect(self.__model.tick)

        layoutContainer.addWidget(self.__fourier_main)
        return centralWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QFApp()
    w.show()
    sys.exit(app.exec())
