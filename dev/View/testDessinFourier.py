# import sys
# from PySide6.QtCore import Qt, QPoint, QRectF, QFile, QSize
# from PySide6.QtGui import QPainter, QPen, QBrush, QPaintDevice
# from PySide6.QtSvg import QSvgGenerator
# from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QFileDialog
#
#
# class DrawingWidget(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.path = []
#         self.is_drawing = False
#
#     def mousePressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self.is_drawing = True
#             self.path.append([event.position()])
#             self.update()
#
#     def mouseMoveEvent(self, event):
#         if self.is_drawing:
#             self.path[-1].append(event.position())
#             self.update()
#
#     def mouseReleaseEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self.is_drawing = False
#
#     def paintEvent(self, event):
#         painter = QPainter(self)
#         pen = QPen(Qt.black, 2, Qt.SolidLine)
#         painter.setPen(pen)
#         for line in self.path:
#             for i in range(1, len(line)):
#                 painter.drawLine(line[i - 1], line[i])
#
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.drawing_widget = DrawingWidget()
#         self.setCentralWidget(self.drawing_widget)
#         self.setGeometry(100, 100, 800, 800)  # Taille de la fenêtre
#         self.setWindowTitle("Dessiner avec PySide6")
#
#         # Création d'un bouton pour sauvegarder le dessin en SVG
#         save_button = QPushButton('Enregistrer en SVG', self)
#         save_button.clicked.connect(self.save_svg)
#         # save_button.setGeometry(QRectF(20, 750, 150, 30))
#
#     def save_svg(self):
#         file_name, _ = QFileDialog.getSaveFileName(self, 'Enregistrer sous', '', 'SVG (*.svg)')
#         if file_name:
#             svg_generator = QSvgGenerator()
#             svg_generator.setFileName(file_name)
#             svg_generator.setSize(QSize(800, 800))
#             svg_generator.setViewBox(QRectF(0, 0, 800, 800))
#             painter = QPainter()
#             painter.begin(svg_generator)
#             self.drawing_widget.render(painter)
#             painter.end()
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())