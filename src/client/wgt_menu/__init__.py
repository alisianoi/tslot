from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from src.common.dto.menu import *


class TMenuWidget(QWidget):

    requested = pyqtSignal(TMenuRequest)

    def __init__(self, parent: QObject=None) -> None:

        super().__init__(parent)

        self.home = QPushButton('Home')
        self.data = QPushButton('Data')
        self.settings = QPushButton('Settings')
        self.about = QPushButton('About')

        self.home.clicked.connect(
            lambda: self.requested.emit(THomeMenuRequest())
        )
        self.data.clicked.connect(
            lambda: self.requested.emit(TDataMenuRequest())
        )
        self.settings.clicked.connect(
            lambda: self.requested.emit(TSettingsMenuRequest())
        )
        self.about.clicked.connect(
            lambda: self.requested.emit(TAboutMenuRequest())
        )

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 0, 0, 0)

        self.layout.addWidget(self.home)
        self.layout.addWidget(self.data)
        self.layout.addWidget(self.settings)
        self.layout.addWidget(self.about)

        self.layout.addStretch(1)

        self.setLayout(self.layout)


class TDockMenuWidget(QDockWidget):

    def __init__(self, parent: QObject=None) -> None:

        super().__init__(parent)

        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.setAllowedAreas(Qt.LeftDockWidgetArea)

        self.setWidget(TMenuWidget(self))

    @pyqtSlot()
    def toggle_menu(self):

        if (self.isHidden()):
            self.show()
        else:
            self.hide()
