#!/usr/bin/env python

import logging
import logging.config
import sys
from functools import wraps
from pathlib import Path
from typing import Any, List, Tuple

from pendulum import datetime
from PyQt5.QtCore import (QAbstractItemModel, QAbstractListModel,
                          QAbstractTableModel, QLocale, QModelIndex, QObject,
                          QSize, QStringListModel, Qt, QTime, QVariant,
                          pyqtSlot)
from PyQt5.QtGui import QFont, QIcon, QPainter, QValidator
from PyQt5.QtWidgets import (QAbstractItemDelegate, QAbstractItemView,
                             QApplication, QCompleter, QFrame, QHBoxLayout,
                             QHeaderView, QItemEditorFactory, QLineEdit,
                             QListView, QMainWindow, QPushButton, QSizePolicy,
                             QStyledItemDelegate, QStyleOptionViewItem,
                             QTableView, QTimeEdit, QVBoxLayout, QWidget)


def logged(foo, logger=logging.getLogger('poc')):
    '''
    Decorate a function and surround its call with enter/leave logs

    Produces logging output of the form:
    > enter foo
      ...
    > leave foo (returned value)
    '''

    @wraps(foo)
    def wrapper(*args, **kwargs):
        logger.debug(f'enter {foo.__qualname__}')

        result = foo(*args, **kwargs)

        logger.debug(f'leave {foo.__qualname__} ({result})')

        return result

    return wrapper


def seconds_to_hh_mm_ss(seconds: int) -> List[int]:
    SECONDS_PER_HOUR = 3600
    SECONDS_PER_MINUTE = 60

    hh = seconds // SECONDS_PER_HOUR
    mm = seconds % SECONDS_PER_HOUR // SECONDS_PER_MINUTE
    ss = seconds % SECONDS_PER_MINUTE

    return [hh, mm, ss]


def seconds_to_str(seconds: int) -> str:
    hh, mm, ss = seconds_to_hh_mm_ss(seconds)

    return f'{hh: >2d}:{mm:0>2d}:{ss:0>2d}'


class TypographyService:

    instances = 0

    @logged
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


class TTimerPopupDelegate(QStyledItemDelegate):

    @logged
    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

    def itemEditorFactory() -> QItemEditorFactory:

        print('delegate.itemEditorFactory')

        return super().itemEditorFactory()

    def setItemEditorFactory(self, factory: QItemEditorFactory) -> None:

        print('delegate.setItemEditorFactory')

        super().setItemEditorFactory(factory)

    def paint(
        self
        , painter: QPainter
        , option : QStyleOptionViewItem
        , index  : QModelIndex
    ) -> None:

        print('delegate.paint()')

        super().paint(painter, option, index)

    def sizeHint(
        self
        , option: QStyleOptionViewItem
        , index : QModelIndex
    ) -> QSize:

        size = super().sizeHint(option, index)

        return QSize(size.width(), 64)
        # return super().sizeHint(option, index)

    def createEditor(
        self
        , parent : QWidget
        , options: QStyleOptionViewItem
        , index  : QModelIndex
    ) -> QWidget:

        print('delegate.createEditor')

        editor = QLineEdit(parent)
        editor.setText(index.data())
        editor.setFont(Typography.font('Quicksand-Medium', 12))

        return editor

    def setEditorData(self, editor: QWidget, index : QModelIndex) -> None:

        print(f'delegate.setEditorData')

        editor.setText(index.data())

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex) -> None:

        print('delegate.setModelData')

        super().setModelData(editor, model, index)

    def updateEditorGeometry(self, editor: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> None:

        print('delegate.updateEditorGeometry')

        super().updateEditorGeometry(editor, option, index)


class TTimerPopupView(QListView):

    @logged
    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.timer_delegate = TTimerPopupDelegate(self)
        self.setItemDelegateForColumn(0, self.timer_delegate)

        self.setFont(Typography.font('Quicksand-Medium', 12))
        self.setFrameStyle(QFrame.NoFrame)


class TTimerListModel(QAbstractListModel):

    @logged
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

    @logged
    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.popup_view = TTimerPopupView()

        self.setPopup(self.popup_view)


class TTimerLineEdit(QLineEdit):

    @logged
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

    @logged
    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.active = False

        self.svg_play = Typography.icon('Fontawesome-Solid', 'play.svg')
        self.svg_stop = Typography.icon('Fontawesome-Solid', 'stop.svg')

        self.timer_mdl = TTimerListModel(self)
        self.timer_cmp = TTimerCompleter(self)
        self.timer_cmp.setModel(self.timer_mdl)

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


class TTimerTableTimeValidator(QValidator):

    @logged
    def __init__(self, parent: QObject=None) -> None:

        super().__init__(parent)

    def validate(
        self
        , input: str
        , pos  : int
    ) -> Tuple[QValidator.State, str, int]:

        print(f'validator.validate({input}, {pos})')

        values = input.split(':')

        if len(values) != 2:
            return (QValidator.Intermediate, input, pos)

        hour, minute = values

        try:
            hour, minute = int(hour), int(minute)
        except ValueError:
            return (QValidator.Invalid, input, pos)

        if hour not in range(0, 24) or minute not in range(0, 60):
            return (QValidator.Invalid, input, pos)

        return (QValidator.Acceptable, input, pos)


class TTableDelegate(QStyledItemDelegate):

    def createEditor(
        self
        , parent : QWidget
        , options: QStyleOptionViewItem
        , index  : QModelIndex
    ) -> QWidget:

        col = index.column()

        if col in range(0, 4):
            editor = QLineEdit(parent)
            editor.setText(index.data())
            editor.setFont(Typography.font('Quicksand-Medium', 12))
        else:
            raise RuntimeError('createEditor')

        if col in range(1, 3):
            editor.setValidator(TTimerTableTimeValidator(editor))

        return editor

    def setEditorData(self, editor: QWidget, index : QModelIndex) -> None:

        if index.column() in range(0, 4):
            editor.setText(index.data())
        else:
            raise RuntimeError('setEditorData')

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

        print('table delegate: sizeHint')

        return super().sizeHint(option, index)


class TTableModel(QAbstractTableModel):

    @logged
    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.tdata = [
            # [
            #     'Far From the Madding Crowd'
            #     , datetime(2018, 9, 25, 13, 42, 18)
            #     , datetime(2018, 9, 25, 13, 48, 29)
            #     , ['read', 'relax']
            # ]
            # , [
            #     'Crime and Punishment'
            #     , datetime(2018, 9, 25, 10, 11, 37)
            #     , datetime(2018, 9, 25, 12, 12, 56)
            #     , ['read', 'tense']
            # ]
        ]

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:

        return Qt.ItemIsEditable | super().flags(index)

    def rowCount(self, parent: QModelIndex=None):
        if not self.tdata:
            return 0
        return len(self.tdata)

    def columnCount(self, parent: QModelIndex=None):
        if not self.tdata or not self.tdata[0]:
            return 0
        return 4

    @logged
    def data(
        self
        , index: QModelIndex=None
        , role : int=Qt.DisplayRole
    ) -> QVariant:

        if not index.isValid():
            return QVariant()

        if role == Qt.DisplayRole:
            return self.data_display_role(index)
        if role == Qt.FontRole:
            return Typography.font('Quicksand-Medium', 12)

        return QVariant()

    def data_display_role(self, index: QModelIndex) -> QVariant:

        if not index.isValid():
            return QVariant()

        fst_ind, lst_ind = 1, 2
        row, col = index.row(), index.column()

        if col == 0:
            return self.tdata[row][col]
        elif col in [fst_ind, lst_ind]:
            value = self.tdata[row][col]
            return '{: >2d}:{:0>2d}'.format(value.hour, value.minute)
        elif col == 3:
            period = self.tdata[row][lst_ind] - self.tdata[row][fst_ind]
            return seconds_to_str(int(period.total_seconds()))

    def setData(
        self
        , index: QModelIndex
        , value: QVariant
        , role : int=Qt.EditRole
    ) -> bool:

        if role != Qt.EditRole:
            return False

        row, col = index.row(), index.column()

        if col == 0:
            self.tdata[row][col] = value
        elif col in range(1, 3):
            old_value = self.tdata[row][col]
            hour, minute = map(int, value.split(':'))
            new_value = old_value.set(hour=hour, minute=minute)
            self.tdata[row][col] = new_value

        return True


class TTableHeaderView(QHeaderView):
    '''
    Control size/resize of headers

    Note:
        https://stackoverflow.com/q/48361795/1269892
    '''

    @logged
    def __init__(
            self
            , orientation: Qt.Orientation=Qt.Horizontal
            , parent     : QWidget=None
    ):
        super().__init__(orientation, parent)

        self.logger = logging.getLogger('tslot')

        self.section_resize_modes = [
            QHeaderView.Stretch # name of task
            , QHeaderView.ResizeToContents # start time
            , QHeaderView.ResizeToContents # finish time
            , QHeaderView.ResizeToContents # elapsed time
        ]

        self.setFrameShape(QFrame.NoFrame)

    @logged
    def setModel(self, model: QAbstractItemModel=None):
        '''
        Set the underlying data model

        Fine-grained resizing of individual sections requires calling
        setSectionResizeMode which works only when you've set the model.
        '''

        if model is None:
            raise RuntimeError('Must provide a model')

        super().setModel(model)

        if self.count() == 0:
            return # if the model is empty, nothing to adjust

        if self.count() != model.columnCount():
            raise RuntimeError('self.count() != model.columnCount()')
        if self.count() != len(self.section_resize_modes):
            raise RuntimeError('self.count() != len(self.section_resize_modes)')

        # The loop below is the only reason why this method exists
        for i, mode in enumerate(self.section_resize_modes):
            self.setSectionResizeMode(i, mode)


class TTableView(QTableView):

    @logged
    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.table_dgt = TTableDelegate(self)
        self.table_hdr = TTableHeaderView(Qt.Horizontal, self)

        # self.setItemDelegate(self.table_delegate)

        self.setFont(Typography.font('Quicksand-Medium', 12))

        # self.setShowGrid(False)

        self.setFrameShape(QFrame.NoFrame)
        self.verticalHeader().hide()
        self.horizontalHeader().hide()

    @logged
    def setModel(self, model: QAbstractItemModel):

        super().setModel(model)

        self.table_hdr.setModel(model)
        self.setHorizontalHeader(self.table_hdr)
        self.horizontalHeader().hide()

    @logged
    def sizeHint(self):
        '''
        Adjust the size of the table to the number of rows it currently holds
        '''

        size_hint = super().sizeHint()

        vheader = self.verticalHeader()

        height = 0 if vheader.isHidden() else vheader.height()

        for i in range(vheader.count()):
            if not vheader.isSectionHidden(i):
                height += vheader.sectionSize(i)

        return QSize(size_hint.width(), height)

    def minimumSizeHint(self):
        return self.sizeHint()


class TTimerTable(QWidget):
    '''
    Combine a table of time slots and a header with date and total time
    '''

    @logged
    def __init__(self, parent: QWidget=None) -> None:

        super().__init__(parent)


class TCentralWidget(QWidget):

    @logged
    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.timer_view = TTimerView(self)

        self.table_view = TTableView(self)
        self.table_model = TTableModel(self)

        self.table_view.setModel(self.table_model)

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.timer_view)
        self.layout.addSpacing(64)
        self.layout.addWidget(self.table_view)

        self.layout.addStretch(1)

        self.setLayout(self.layout)


class TMainWindow(QMainWindow):

    @logged
    def __init__(self):
        super().__init__()

        self.central_widget = TCentralWidget(self)
        self.setCentralWidget(self.central_widget)

if __name__ == '__main__':

    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'verbose': {
                'format': '%(asctime)22s %(levelname)7s %(module)10s %(process)6d %(thread)15d %(message)s'
            }
            , 'simple': {
                'format': '%(levelname)s %(message)s'
            }
        }
        , 'handlers': {
            'console': {
                'level': 'DEBUG'
                , 'class': 'logging.StreamHandler'
                , 'formatter': 'verbose'
            }
            #, 'file': {
            #     'level': 'DEBUG'
            #     , 'class': 'logging.handlers.RotatingFileHandler'
            #     , 'formatter': 'verbose'
            #     , 'filename': 'tslot.log'
            #     , 'maxBytes': 10485760 # 10 MiB
            #     , 'backupCount': 3
            # }
        },
        'loggers': {
            'poc': {
                'handlers': ['console']
                , 'level': 'DEBUG',
            }
        }
    })

    logger = logging.getLogger('poc')
    logger.debug('PoC logger up and running')

    app = QApplication(sys.argv)

    main_window = TMainWindow()
    main_window.show()

    sys.exit(app.exec())
