#!/usr/bin/env python

import sys

from PyQt5.QtCore import (QAbstractItemModel, QAbstractListModel,
                          QAbstractTableModel, QModelIndex, QObject, QSize,
                          QStringListModel, Qt, QVariant)
from PyQt5.QtWidgets import (QApplication, QCompleter, QHBoxLayout, QLineEdit,
                             QMainWindow, QPushButton, QTableView, QVBoxLayout,
                             QWidget)


class TTimerListModel(QAbstractListModel):

    def __init__(self, parent: QObject=None) -> None:

        super().__init__(parent)

        self.tdata = ['Aleksandr Lisianoi', 'Apples', 'Lime']

    def rowCount(self, parent: QModelIndex) -> int:

        if parent.isValid():
            # a list model expects all of its items to be "top level", i.e. not
            # to have any parents, i.e. to be supplied an invalid index. If the
            # index is valid for some reason, raise:
            raise RuntimeError('TTimerListModel needs an invalid parent index')

        return len(self.tdata)

    def data(self, index: QModelIndex, role: int=Qt.DisplayRole) -> QVariant:

        if not index.isValid():
            raise RuntimeError('TTimerListModel needs a valid data index')

        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self.tdata[index.row()]

        return None


class TTimerCompleter(QCompleter):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)


class TTimerLineEdit(QLineEdit):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.setPlaceholderText('Your current task')
        self.setClearButtonEnabled(True)

        self.setFrame(False)


class TTimerPushButton(QPushButton):

    pass


class TTimerView(QWidget):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.timer_mdl = TTimerListModel(self)
        self.timer_cmp = TTimerCompleter(self.timer_mdl)

        self.timer_cmp.setModel(self.timer_mdl)

        self.timer_ldt = TTimerLineEdit(self)
        self.timer_btn = TTimerPushButton(self)

        self.timer_ldt.setCompleter(self.timer_cmp)

        self.layout = QHBoxLayout()

        self.layout.addWidget(self.timer_ldt)
        self.layout.addWidget(self.timer_btn)

        self.setLayout(self.layout)


class TTableModel(QAbstractTableModel):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.tdata = [
              ['row0, col0 (expanding)', 'row0, col1 (expanding)', 'row0, col2']
            , ['row1, col0 (expanding)', 'row1, col1 (expanding)', 'row1, col2']
            , ['row2, col0 (expanding)', 'row2, col1 (expanding)', 'row2, col2']
        ]

    def rowCount(self, parent: QModelIndex=None):
        return 2

    def columnCount(self, parent: QModelIndex=None):
        return 2

    def data(self, index: QModelIndex=None, role: int=Qt.DisplayRole):

        return QVariant()


class TTableView(QTableView):

    pass


class TCentralWidget(QWidget):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.timer_view = TTimerView(self)

        self.table_view = TTableView(self)
        self.table_model = TTableModel(self)

        self.table_view.setModel(self.table_model)

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.timer_view)
        self.layout.addWidget(self.table_view)

        self.layout.addStretch(1)

        self.setLayout(self.layout)


class TMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.central_widget = TCentralWidget(self)
        self.setCentralWidget(self.central_widget)

if __name__ == '__main__':

    app = QApplication(sys.argv)

    main_window = TMainWindow()
    main_window.show()

    sys.exit(app.exec())
