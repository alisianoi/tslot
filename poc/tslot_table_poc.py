#!/usr/bin/env python

import sys
from pathlib import Path

from PyQt5.QtCore import (QAbstractItemModel, QAbstractListModel,
                          QAbstractTableModel, QModelIndex, QObject, QSize,
                          QStringListModel, Qt, QVariant, pyqtSlot)
from PyQt5.QtGui import QFont, QIcon, QPainter
from PyQt5.QtWidgets import (QAbstractItemDelegate, QAbstractItemView,
                             QApplication, QCompleter, QHBoxLayout, QLineEdit,
                             QMainWindow, QPushButton, QStyledItemDelegate,
                             QStyleOptionViewItem, QTableView, QVBoxLayout,
                             QWidget)


class TypographyService:

    instances = 0

    def __init__(self):

        TypographyService.instances += 1

        self.font_path = Path(Path.cwd(), '..', 'font').resolve()

        self.fontawesome_svgs_solid = Path(
            Path.cwd(), '..', 'font', 'fontawesome', 'svgs', 'solid'
        ).resolve()

        self.quicksand_path = Path(self.font_path, 'Quicksand')
        self.quicksand_medium = Path(
            self.quicksand_path, 'Quicksand-Medium.ttf'
        )
        self.quicksand_regular = Path(
            self.quicksand_path, 'Quicksand-Regular.ttf'
        )

        self.supported_fonts = {
            'Quicksand-Medium' : self.quicksand_medium
            , 'Quicksand-Regular': self.quicksand_regular
        }

        self.supported_icons = {
            'Fontawesome-Solid': self.fontawesome_svgs_solid
        }

    def font(self, family: str, size: int) -> QFont:

        try:
            return QFont(str(self.supported_fonts[family]), size)
        except KeyError:
            print(f'No such font: {family}, {size}')
            return QFont()

    def icon(self, family: str, name: str) -> QIcon:
        '''
        Return a QIcon that uses the provided font family and icon name

        :param family: the font family to use
        :param icon: the icon name
        '''

        try:
            return QIcon(str(Path(self.supported_icons[family], name)))
        except KeyError:
            print(f'No such icon: {family}, {name}')
            return QIcon()


Typography = TypographyService()


class TTimerPopupDelegate(QAbstractItemDelegate):

    def paint(
        self
        , painter: QPainter
        , option: QStyleOptionViewItem
        , index: QModelIndex
    ) -> None:

        super().paint(painter, option, index)


class TTimerPopupView(QAbstractItemView):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.timer_delegate = TTimerPopupDelegate(self)

        self.setItemDelegate(self.timer_delegate)

    def verticalOffset(self):

        return 16 # random number

    def horizontalOffset(self):

        return 16 # random number


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

        self.setFrame(False)
        self.setPlaceholderText('Your current task')


class TTimerPushButton(QPushButton):

    pass


class TTimerView(QWidget):
    '''
    Combine a timer line edit with a timer push button and current timer value
    '''

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.active = False

        self.svg_play = Typography.icon('Fontawesome-Solid', 'play.svg')
        self.svg_stop = Typography.icon('Fontawesome-Solid', 'stop.svg')

        self.timer_mdl = TTimerListModel(self)
        self.timer_pop = TTimerPopupView(self)
        self.timer_cmp = TTimerCompleter(self.timer_mdl)
        self.timer_cmp.setModel(self.timer_mdl)
        self.timer_cmp.setPopup(self.timer_pop)

        self.timer_ldt = TTimerLineEdit(self)
        self.timer_ldt.setMinimumHeight(64)
        self.timer_ldt.setFont(Typography.font('Quicksand-Medium', 12))
        self.timer_ldt.setCompleter(self.timer_cmp)

        self.timer_btn = TTimerPushButton(self)
        self.timer_btn.setIcon(self.svg_play)
        self.timer_btn.setMinimumSize(64, 64)
        self.timer_btn.setFlat(True)

        self.layout = QHBoxLayout()

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.layout.addWidget(self.timer_ldt)
        self.layout.addWidget(self.timer_btn)

        self.setLayout(self.layout)

        self.timer_btn.clicked.connect(self.handle_timer_btn_clicked)

    @pyqtSlot()
    def handle_timer_btn_clicked(self):

        if self.active:
            self.active = False
            self.timer_btn.setIcon(self.svg_play)
        else:
            self.active = True
            self.timer_btn.setIcon(self.svg_stop)


class TTableDelegate(QStyledItemDelegate):

    def createEditor(
        self
        , parent : QWidget
        , options: QStyleOptionViewItem
        , index  : QModelIndex
    ) -> QWidget:

        editor = QLineEdit(parent)
        editor.setText(index.data())
        editor.setFont(Typography.font('Quicksand-Medium', 12))

        return editor

        # return super().createEditor(parent, options, index)

    def setEditorData(self, editor: QWidget, index : QModelIndex) -> None:

        print(f'index')
        editor.setText(index.data())

    # def setModelData(
    #     self
    #     , editor: QWidget
    #     , model : QAbstractItemModel
    #     , index : QModelIndex
    # ) -> None:
    #
    #     super().setModelData(editor, model, index)

    # def updateEditorGeometry(
    #     self
    #     , parent : QWidget
    #     , options: QStyleOptionViewItem
    #     , index  : QModelIndex
    # ) -> QWidget:
    #
    #     super().updateEditorGeometry(parent, options, index)

    # from the stars tutorial:

    def paint(
        self
        , painter: QPainter
        , option : QStyleOptionViewItem
        , index  : QModelIndex
    ) -> None:

        super().paint(painter, option, index)

    def sizeHint(
        self
        , option: QStyleOptionViewItem
        , index : QModelIndex
    ) -> QSize:

        return super().sizeHint(option, index)

class TTableModel(QAbstractTableModel):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.tdata = [
              ['Hello', 'world']
              , ['Fish', 'Chips']
        ]

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:

        return Qt.ItemIsEditable | super().flags(index)

    def rowCount(self, parent: QModelIndex=None):
        return len(self.tdata)

    def columnCount(self, parent: QModelIndex=None):
        return len(self.tdata[0]) if self.tdata[0] else 0

    def data(self, index: QModelIndex=None, role: int=Qt.DisplayRole):

        if not index.isValid():
            return QVariant()

        if role == Qt.DisplayRole:
            return self.tdata[index.row()][index.column()]
        if role == Qt.FontRole:
            return Typography.font('Quicksand-Medium', 12)

        return QVariant()

    def setData(
        self
        , index: QModelIndex
        , value: QVariant
        , role : int=Qt.EditRole
    ) -> bool:

        if role != Qt.EditRole:
            return False

        self.tdata[index.row()][index.column()] = value

        return True

class TTableView(QTableView):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.table_delegate = TTableDelegate(self)

        self.setItemDelegate(self.table_delegate)

        # self.verticalHeader().hide()
        # self.horizontalHeader().hide()


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
