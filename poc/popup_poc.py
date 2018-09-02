#!/usr/bin/env python

import logging
import logging.config
import sys
import time
from functools import wraps

from PyQt5.QtCore import QObject, QPoint, QRect, QSize, Qt, QTimer, pyqtSlot
from PyQt5.QtGui import (QBrush, QCloseEvent, QColor, QGuiApplication,
                         QHideEvent, QKeySequence, QMoveEvent, QPainter,
                         QPaintEvent, QResizeEvent, QScreen, QShowEvent)
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
                             QPushButton, QShortcut, QVBoxLayout, QWidget)


def logged(logger=logging.getLogger('poc'), disabled=False):
    '''
    Create a configured decorator that controls logging output of a function

    :param logger: the logger to send output to
    :param disabled: True if the logger should be disabled, False otherwise
    '''

    def logged_decorator(foo):
        '''
        Decorate a function and surround its call with enter/leave logs

        Produce logging output of the form:
        > enter foo
          ...
        > leave foo (returned value)
        '''

        @wraps(foo)
        def wrapper(*args, **kwargs):

            was_disabled = logger.disabled

            # If the logger was not already disabled by something else, see if
            # it should be disabled by us. Important effect: if foo uses the
            # same logger, then any inner logging will be disabled as well.
            if not was_disabled:
                logger.disabled = disabled

            logger.debug(f'enter {foo.__qualname__}')

            result = foo(*args, **kwargs)

            logger.debug(f'leave {foo.__qualname__} ({result})')

            # Restore previous logger state:
            logger.disabled = was_disabled

            return result

        return wrapper

    return logged_decorator


class TCentralWidget(QWidget):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.logger = logging.getLogger('poc')

        self.popup_btn = QPushButton('Click for a popup')

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.popup_btn)
        self.setLayout(self.layout)

        self.setStyleSheet('background-color: #8B0000')

        self.logger.debug(self.parent())
        self.popup_btn.clicked.connect(self.parent().handle_shortcut_new_pop)

    @logged(disabled=True)
    def paintEvent(self, event: QPaintEvent) -> None:

        self.logger.debug(f'{event.rect()} and {event.region()}')

        super().paintEvent(event)

    @logged(disabled=True)
    def resizeEvent(self, event: QResizeEvent):

        parent = self.parentWidget()
        if parent is None:
            self.logger.debug('has no parent')
        else:
            self.logger.debug(f'parent.geometry: {parent.geometry()}')

        self.logger.debug(f'{event.oldSize()} -> {event.size()}')

        super().resizeEvent(event)


class TSideWidget(QWidget):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.logger = logging.getLogger('poc')

        self.label = QLabel('Click this: ')
        self.woops = QPushButton('Undo')
        self.close = QPushButton('Close')

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.woops)
        self.layout.addWidget(self.close)
        self.setLayout(self.layout)

        self.setWindowFlags(Qt.Popup)

    def __del__(self) -> None:

        self.logger.debug('__del__')

    @logged(disabled=False)
    def showEvent(self, event: QShowEvent) -> None:

        super().showEvent(event)

        self.logger.debug(f'showEvent: {event.spontaneous()}')

    @logged(disabled=False)
    def hideEvent(self, event: QHideEvent) -> None:

        super().hideEvent(event)

        self.logger.debug(f'hideEvent: {event.spontaneous()}')

    @logged(disabled=False)
    def moveEvent(self, event: QMoveEvent) -> None:

        super().moveEvent(event)

        self.logger.debug(f'{event.oldPos()} -> {event.pos()}')

    @logged(disabled=False)
    def paintEvent(self, event: QPaintEvent) -> None:

        super().paintEvent(event)

        self.logger.debug(f'event.rect(): {event.rect()}')

    @logged(disabled=False)
    def closeEvent(self, event: QCloseEvent) -> None:

        super().closeEvent(event)

        self.logger.debug(f'closeEvent(): {event.spontaneous()}')

    @logged(disabled=False)
    def resizeEvent(self, event: QResizeEvent) -> None:

        super().resizeEvent(event)

        self.logger.debug(f'{event.oldSize()} -> {event.size()}')

    def deleteLater(self) -> None:

        super().deleteLater()

        self.logger.debug('delete later')


class TMainWindow(QMainWindow):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.logger = logging.getLogger('poc')

        self.sidepop_widget = None

        self.central_widget = TCentralWidget(self)
        self.setCentralWidget(self.central_widget)

        self.shortcut_new_pop = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_N), self)
        self.shortcut_new_wgt = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_P), self)

        self.shortcut_new_pop.activated.connect(self.handle_shortcut_new_pop)
        self.shortcut_new_wgt.activated.connect(self.handle_shortcut_new_wgt)

        self.setStyleSheet('background-color: #00008B')

    @logged()
    @pyqtSlot()
    def handle_shortcut_new_pop(self):

        if self.sidepop_widget is None:
            self.sidepop_widget = TSideWidget()
            self.sidepop_widget.show()
        else:
            self.sidepop_widget.hide()
            self.sidepop_widget.deleteLater()
            self.sidepop_widget = None

    def handle_shortcut_new_wgt(self):

        self.logger.debug('handle shortcut new wgt')

        if (self.central_widget.isHidden()):
            self.central_widget.show()
        else:
            self.central_widget.hide()

    @logged(disabled=True)
    def paintEvent(self, event: QPaintEvent) -> None:

        self.logger.debug(f'{event.rect()} and {event.region()}')

        super().paintEvent(event)

    @logged(disabled=True)
    def resizeEvent(self, event: QResizeEvent) -> None:

        parent = self.parentWidget()
        if parent is None:
            self.logger.debug('has no parent')
        else:
            self.logger.debug(f'parent.geometry: {parent.geometry()}')

        self.logger.debug(f'{event.oldSize()} -> {event.size()}')

        super().resizeEvent(event)


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

    app = QApplication(sys.argv)

    main_window = TMainWindow()
    main_window.show()

    sys.exit(app.exec())
