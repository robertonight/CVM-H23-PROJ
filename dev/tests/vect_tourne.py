import sys
import math
from PySide6.QtCore import QPointF, QTimer
from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsLineItem
from PySide6.QtGui import QPen, QColor, QPainter


class RotatingVectors:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.view = QGraphicsView()
        self.view.setRenderHint(QPainter.Antialiasing)
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.view.setFixedSize(300, 300)
        self.view.setSceneRect(-400, -400, 800, 800)

        # Créer les vecteurs
        self.vector1 = QGraphicsLineItem(0, 0, 100, 0)
        self.vector2 = QGraphicsLineItem(0, 0, 50, 0)

        # Configurer les vecteurs
        pen = QPen(QColor("black"), 2)
        self.vector1.setPen(pen)
        self.vector2.setPen(pen)
        self.scene.addItem(self.vector1)
        self.scene.addItem(self.vector2)

        # Configurer le timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate_vectors)
        self.timer.start(16)  # 16 ms pour environ 60 FPS
        self.angle = 0

    def rotate_vectors(self):
        self.angle += 1

        # Rotation du premier vecteur
        x1 = 100 * math.cos(math.radians(self.angle))
        y1 = 100 * math.sin(math.radians(self.angle))
        self.vector1.setLine(0, 0, x1, y1)

        # Position et rotation du second vecteur
        vector1_end = self.vector1.line().p2()
        x2 = 50 * math.cos(math.radians(2 * self.angle))
        y2 = 50 * math.sin(math.radians(2 * self.angle))
        self.vector2.setPos(vector1_end)
        self.vector2.setLine(0, 0, x2, y2)

    def run(self):
        self.view.show()
        sys.exit(self.app.exec())


if __name__ == "__main__":
    rotating_vectors = RotatingVectors()
    rotating_vectors.run()
