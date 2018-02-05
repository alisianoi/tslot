#!/usr/bin/env python

import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class MyTableModel(QAbstractTableModel):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.messages = [['hello', 'world']]

    def headerData(
        self
        , section    : int
        , orientation: Qt.Orientation
        , role       : Qt.ItemDataRole=Qt.DisplayRole
    ):
        if orientation == Qt.Vertical:
            return QVariant()

        if role == Qt.DisplayRole:
            if section == 0:
                return 'Message'
            if section == 1:
                return 'Index'

        return QVariant()

    def data(
        self
        , index: QModelIndex=QModelIndex()
        , role : Qt.ItemDataRole=Qt.DisplayRole
    ):
        if not index.isValid():
            return QVariant()
        if role != Qt.DisplayRole:
            return QVariant()

        return self.messages[index.row()][index.column()]
        
    def rowCount(self, parent: QModelIndex=QModelIndex()):
        return len(self.messages)

    def columnCount(self, parent: QModelIndex=QModelIndex()):
        return 2


class MyTableView(QTableView):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)


class MyCentralWidget(QWidget):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.my_table_model = MyTableModel(parent=parent)

        self.my_table_view = MyTableView(parent=parent)
        self.my_table_view.setModel(self.my_table_model)

        self.push_btn = QPushButton('Remove model')
        self.push_btn.clicked.connect(self.remove_model)

        self.layout = QVBoxLayout(self)

        self.layout.addWidget(self.my_table_view)
        self.layout.addWidget(self.push_btn)

        self.setLayout(self.layout)

    @pyqtSlot()
    def remove_model(self):
        print(self.my_table_view)
        self.my_table_view.deleteLater()

        print('above sleep')
        QThread.currentThread().sleep(3)
        print('below sleep')
        print(self.my_table_view)


class MyMainWindow(QMainWindow):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.central_widget = MyCentralWidget(self)

        self.setCentralWidget(self.central_widget)


if __name__ == '__main__':

    app = QApplication(sys.argv)

    main_window = MyMainWindow()
    main_window.show()

    sys.exit(app.exec())



