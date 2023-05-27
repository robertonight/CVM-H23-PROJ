# nom du fichier: main.py
#
# Ce fichier contient la classe QFApp qui est la fenêtre principale, ainsi que la fonction main qui
# est la fonction principale appelée pour lancer le programme.
#
# Auteurs: Patrice Gallant et Roberto Nightingale


import sys

from PySide6.QtCore import Slot
from PySide6.QtWidgets import (QMainWindow, QApplication, QWidget, QHBoxLayout)
from gui_left_window import LeftWindow
from gui_fourier import GuiFourierMain
from model import Model
from gui_feed import GuiFeedMain


class QFApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.__model = None
        self.setWindowTitle("C'est fou. Riez!")
        self.resize(1250, 900)
        self.__fourierMain = None
        self.init_gui()
        # ref: https://stackoverflow.com/questions/7351493/how-to-add-border-around-qwidget
        self.setStyleSheet(
            "QFrame {border: 1px solid black;} * {background-color: rgb(150,150,150);} QLabel {border: 0px}")

    def init_gui(self):
        # declarations
        self.__model = Model()
        __centralWidget = self.change_to_fourier_windows()
        self.setCentralWidget(__centralWidget)

    @Slot()
    def erase_drawing(self):
        self.__leftWindow.erase_drawing()
        self.__fourierMain.erase_drawing()

    @Slot()
    def change_to_feed(self):
        self.__fourierMain.stop_sim()
        self.__model.stop_sim()
        __drawings = self.__model.get_drawings()
        __newCentralWidget = GuiFeedMain(__drawings)
        __newCentralWidget.return_pushed.connect(self.quit_feed)
        __newCentralWidget.display_right_clicked.connect(self.set_chosen_drawing)
        self.setCentralWidget(__newCentralWidget)

    @Slot()
    def set_chosen_drawing(self, drawing):
        self.quit_feed()
        self.__leftWindow.set_drawing(drawing)
        self.__model.set_drawing(drawing)

    @Slot()
    def quit_feed(self):
        __newCentralWidget = self.change_to_fourier_windows()
        self.setCentralWidget(__newCentralWidget)

    def change_to_fourier_windows(self):
        __centralWidget = QWidget()
        __layoutContainer = QHBoxLayout()
        self.__leftWindow = LeftWindow()
        self.__leftWindow.line_ended.connect(self.__model.receive_line)
        self.__leftWindow.undo_pushed.connect(self.__model.undo_line)
        self.__leftWindow.erase_pushed.connect(self.__model.erase_drawing)
        self.__model.drawing_deleted.connect(self.erase_drawing)
        self.__leftWindow.drawing_saved.connect(self.__model.save_drawing)
        self.__leftWindow.cliked_feed.connect(self.change_to_feed)
        # ajout
        __layoutContainer.addWidget(self.__leftWindow)
        __centralWidget.setLayout(__layoutContainer)
        self.__fourierMain = GuiFourierMain(self.__model.nbVectors, self.__model.precision)
        self.__fourierMain.tick.connect(self.__model.tick)
        self.__fourierMain.play_pressed.connect(self.__model.start_sim)
        self.__fourierMain.previous_pressed.connect(self.__model.previous_interval)
        self.__fourierMain.next_pressed.connect(self.__model.next_interval)
        self.__fourierMain.precision_changed.connect(self.__model.change_precision)
        self.__fourierMain.nb_vectors_changed.connect(self.__model.change_nb_vecteurs)
        self.__model.sim_started.connect(self.__fourierMain.start_sim)
        self.__model.sim_updated.connect(self.__fourierMain.update_sim)
        self.__model.new_animation_started.connect(self.__fourierMain.reset_drawing)

        __layoutContainer.addWidget(self.__fourierMain)
        return __centralWidget


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QFApp()
    w.show()
    sys.exit(app.exec())
