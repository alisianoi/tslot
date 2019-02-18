from PyQt5.QtWidgets import QLabel, QWidget


class MyLabel(QLabel):

    def __init__(self, parent: QWidget = None):

        super().__init__(parent)
