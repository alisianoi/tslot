#!/usr/bin/env python
import sys

from PyQt5.QtCore import (QEasingCurve, QParallelAnimationGroup,
                          QPropertyAnimation, QRect, QSize, pyqtSlot)
from PyQt5.QtWidgets import (QApplication, QGraphicsOpacityEffect, QLabel,
                             QLineEdit, QMainWindow, QPushButton, QVBoxLayout,
                             QWidget)


class TLineEdit(QLineEdit):

    def __init__(self, parent: QWidget=None) -> None:

        super().__init__(parent)

        self.setStyleSheet('background-color: #AAAA00')

class TPushButton(QPushButton):

    def __init__(self, parent: QWidget=None) -> None:

        super().__init__(parent)

        self.setStyleSheet('background-color: #AAAA00')

class TLabel(QLabel):

    def __init__(self, parent: QWidget=None) -> None:

        super().__init__(parent)

        self.setStyleSheet('background-color: #8B0000')


class TCentralWidget(QWidget):

    def __init__(self, parent: QWidget=None) -> None:

        super().__init__(parent)

        self.effects = []
        self.animations = []

        # Create widgets
        self.line_edit = TLineEdit()
        self.push_button = TPushButton('Push Me')
        self.label0 = TLabel()
        self.label1 = TLabel()
        self.label2 = TLabel()
        self.label3 = TLabel()

        self.labels = [self.label0, self.label1, self.label2, self.label3]

        # Create layout, add widgets
        self.layout = QVBoxLayout()

        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.push_button)
        self.layout.addWidget(self.label0)
        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.label3)

        self.setLayout(self.layout)

        # Connect signals and slots
        self.push_button.clicked.connect(self.handle_button)

        self.setStyleSheet('background-color: #00008B')

    @pyqtSlot()
    def handle_button(self) -> None:

        self.effects = []
        self.animations = []
        self.animation_group = QParallelAnimationGroup()

        for i in range(4):
            self.effects.append(QGraphicsOpacityEffect())
            self.animations.append(QPropertyAnimation(self.effects[i], b'opacity'))

            self.animations[i].setStartValue(0.0)
            self.animations[i].setEndValue(1.0)
            self.animations[i].setDuration(1000)

            self.labels[i].setGraphicsEffect(self.effects[i])

            self.animation_group.addAnimation(self.animations[i])

        self.animations[0].setEasingCurve(QEasingCurve.OutQuad)
        self.animations[1].setEasingCurve(QEasingCurve.OutCubic)
        self.animations[2].setEasingCurve(QEasingCurve.OutQuint)
        self.animations[3].setEasingCurve(QEasingCurve.OutExpo)

        self.animation_group.start()

class TMainWindow(QMainWindow):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setCentralWidget(TCentralWidget())

if __name__ == '__main__':

    app = QApplication(sys.argv)

    main_window = TMainWindow()
    main_window.show()

    sys.exit(app.exec())
