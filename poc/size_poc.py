#!/usr/bin/env python

import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class MyPushButton(QPushButton):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.setText('Hello, world!')

        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)

    def sizeHint(self):
        return QSize(300, 100)

    def sizePolicy(self):
        return QSizePolicy(Policy.Minimum, Policy.Minimum)


class MyTableModel(QAbstractTableModel):

    def __init__(self, i: int, parent: QObject=None):

        super().__init__(parent)

        self.i = i

    def headerData(
        self
        , section: int
        , orientation: Qt.Orientation
        , role : Qt.ItemDataRole=Qt.DisplayRole
    ):
        if orientation == Qt.Vertical:
            return super().headerData(section, orientation, role)

        if role == Qt.DisplayRole:
            if section == 0:
                return "Secret message"
            if section == 1:
                return "Identification"

        return super().headerData(section, orientation, role)

    def rowCount(self, parent: QModelIndex=QModelIndex()):
        return self.i

    def columnCount(self, parent: QModelIndex=QModelIndex()):
        return 2

    def data(
        self
        , index: QModelIndex=QModelIndex()
        , role : Qt.ItemDataRole=Qt.DisplayRole
    ):
        if role == Qt.SizeHintRole:
            print(f"Asking for size hint on ({row}, {self.i})")
            return super().data(index, role)

        if role != Qt.DisplayRole:
            return QVariant()

        row, column = index.row(), index.column()

        if column == 0:
            return "Here is the message"
        if column == 1:
            return f"{row} out of {self.i}"

        return super().data(index, role)


class MyHHeaderView(QHeaderView):

    def __init__(
            self
            , orientation: Qt.Orientation
            , parent     : QWidget=None
    ):
        super().__init__(orientation, parent)

    def sizeHint(self):
        print('MyHHeaderView.sizeHint')

        dsize = super().sizeHint()
        psize = self.parentWidget().size()

        print(f'dsize: {dsize}; psize: {psize}')
        return QSize(psize.width() / 2, dsize.height())

    def sizePolicy(self):
        print('MyHHeaderView.sizePolicy')

        return super().sizePolicy()

    def sectionSizeHint(self, logicalIndex: int):
        print('MyHHeaderView.sectionSizeHint')

        return super().sectionSizeHint(logicalIndex)

    def sectionResizeMode(self, logicalIndex: int):
        print('MyHHeaderView.sectionResizeMode')

        return super().sectionResizeMode(logicalIndex)


class MyVHeaderView(QHeaderView):

    def __init__(
            self
            , orientation: Qt.Orientation
            , parent     : QWidget=None
    ):
        super().__init__(orientation, parent)

    def sizeHint(self):
        print('MyVHeaderView.sizeHint')

        return super().sizeHint()

    def sizePolicy(self):
        print('MyVHeaderView.sizePolicy')

        return super().sizePolicy()

    def sectionSizeHint(self, logicalIndex: int):
        print('MyVHeaderView.sectionSizeHint')

        return super().sectionSizeHint(logicalIndex)

    def sectionResizeMode(self, logicalIndex: int):
        print('MyVHeaderView.sectionResizeMode')

        return super().sectionResizeMode(logicalIndex)


class MyTableView(QTableView):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.setVerticalHeader(MyVHeaderView(Qt.Vertical, self))
        self.setHorizontalHeader(MyHHeaderView(Qt.Horizontal, self))

    def sizeHint(self):
        print('MyTableView.sizeHint')

        model = self.model()

        if model is None:
            return super().sizeHint()

        nrows = model.rowCount()

        phint = super().sizeHint()

        vheader_shint = self.verticalHeader().sizeHint()

        shint = QSize(phint.width(), 2 * nrows * vheader_shint.height())

        print(f'Will hint {shint} instead of {phint}')

        return shint

    def sizePolicy(self):
        print('MyTableView.sizePolicy')

        return super().sizePolicy()


class MyScrollWidget(QWidget):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.layout = QVBoxLayout()

        for i in range(1, 20):
            view = MyTableView(self)
            model = MyTableModel(i=i, parent=self)

            view.setModel(model)

            self.layout.addWidget(view)

        self.setLayout(self.layout)

    def sizeHint(self):
        print('MyScrollWidget.sizeHint')

        return super().sizeHint()

    def sizePolicy(self):
        print('MyScrollWidget.sizePolicy')

        return super().sizePolicy()


class MyScrollArea(QScrollArea):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.main_widget = MyScrollWidget(self)

        self.setWidget(self.main_widget)
        self.setWidgetResizable(True)

    def sizeHint(self):
        print('MyScrollArea.sizeHint')

        return super().sizeHint()

    def sizePolicy(self):
        print('MyScrollArea.sizePolicy')

        return super().sizePolicy()


class MyCentralWidget(QWidget):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.widget = MyScrollArea(self)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.widget)

        self.setLayout(self.layout)


class MyMainWindow(QMainWindow):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.central_widget = MyCentralWidget(self)

        self.setCentralWidget(self.central_widget)


if __name__ == '__main__':

    app = QApplication(sys.argv)

    main_window = MyMainWindow()
    main_window.show()

    sys.exit(app.exec())
