#!/usr/bin/env python

import logging
import logging.config
import sys
import time
from functools import wraps

from PyQt5.QtCore import (QEasingCurve, QObject, QPoint, QPropertyAnimation,
                          QRect, QSize, Qt, QTimer, pyqtSignal, pyqtSlot)
from PyQt5.QtGui import (QBrush, QCloseEvent, QColor, QGuiApplication,
                         QHideEvent, QKeySequence, QMoveEvent, QPainter,
                         QPaintEvent, QResizeEvent, QScreen, QShowEvent)
from PyQt5.QtWidgets import (QApplication, QGraphicsEffect,
                             QGraphicsOpacityEffect, QHBoxLayout, QLabel,
                             QMainWindow, QPushButton, QShortcut, QStyle,
                             QStyleOption, QVBoxLayout, QWidget)


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

            logger.disabled = disabled

            logger.debug(f'enter {foo.__qualname__}')

            result = foo(*args, **kwargs)

            logger.debug(f'leave {foo.__qualname__} ({result})')

            # Restore previous logger state:
            logger.disabled = was_disabled

            return result

        return wrapper

    return logged_decorator


class TRequest:

    pass

class TSideRequest(TRequest):

    def __init__(self, payload: str) -> None:

        self.payload = payload

class TResponse:

    pass

class TUndoResponse(TResponse):

    def __init__(self, wgt: QWidget):

        self.wgt = wgt

class TCloseResponse(TResponse):

    def __init__(self, wgt: QWidget):

        self.wgt = wgt


class TPopupWidget(QWidget):

    responded = pyqtSignal(TResponse)

    def __init__(self, txt: str, parent: QWidget=None):

        super().__init__(parent)

        self.logger = logging.getLogger('poc')

        self.label = QLabel(txt)
        self.undo_btn = QPushButton('Undo')
        self.close_btn = QPushButton('Close')

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.undo_btn)
        self.layout.addWidget(self.close_btn)
        self.setLayout(self.layout)

        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.setAutoFillBackground(True)

        self.undo_btn.clicked.connect(self.handle_undo)
        self.close_btn.clicked.connect(self.handle_close)

    @pyqtSlot()
    def handle_undo(self):
        self.responded.emit(TUndoResponse(self))

        self.close()

    @pyqtSlot()
    def handle_close(self):
        self.responded.emit(TCloseResponse(self))

        self.close()

    def __del__(self) -> None:

        self.logger.debug('__del__')

    @logged(disabled=True)
    def showEvent(self, event: QShowEvent) -> None:

        super().showEvent(event)

        self.logger.debug(f'showEvent: {event.spontaneous()}')

    @logged(disabled=True)
    def hideEvent(self, event: QHideEvent) -> None:

        super().hideEvent(event)

        self.logger.debug(f'hideEvent: {event.spontaneous()}')

    @logged(disabled=True)
    def moveEvent(self, event: QMoveEvent) -> None:

        super().moveEvent(event)

        self.logger.debug(f'{event.oldPos()} -> {event.pos()}')

    @logged(disabled=True)
    def paintEvent(self, event: QPaintEvent) -> None:

        painter = QPainter(self)
        style, style_option = self.style(), QStyleOption()

        style_option.initFrom(self)

        style.drawPrimitive(QStyle.PE_Widget, style_option, painter, self)

        super().paintEvent(event)

        self.logger.debug(f'event.rect(): {event.rect()}')

    @logged(disabled=True)
    def closeEvent(self, event: QCloseEvent) -> None:

        super().closeEvent(event)

        self.logger.debug(f'closeEvent(): {event.spontaneous()}')

    @logged(disabled=True)
    def resizeEvent(self, event: QResizeEvent) -> None:

        super().resizeEvent(event)

        old_size = event.oldSize()

        if old_size.width() == -1 and old_size.height() == -1:
            # The window manager has just decided on the size of this widget. It
            # means the widget is being shown for the first time. Take it as an
            # opportunity to properly position this notification widget.
            self.logger.debug('looks like a brand new widget')

        self.logger.debug(f'{event.oldSize()} -> {event.size()}')

    @logged(disabled=True)
    def deleteLater(self) -> None:

        super().deleteLater()

        self.logger.debug('delete later')


class TPopupService(QObject):

    def __init__(self, parent: QWidget=None, xgap: int=10, ygap: int=10):

        super().__init__()

        self.logger = logging.getLogger('poc')

        self.parent = parent
        self.popups = []

        self.effects = {}
        self.animations = {}

        self.xgap = xgap
        self.ygap = ygap

    @logged(disabled=True)
    def notify(self, txt: str) -> None:

        popup = TPopupWidget(txt, self.parent)
        popup.responded.connect(self.handle_popup)

        self.enlist(popup)

    @logged(disabled=False)
    def enlist(self, popup: QWidget) -> None:

        x, y = -1, -1

        xgap, ygap = self.xgap, self.ygap

        parent = self.parent
        px, py = parent.x(), parent.y()
        pw, ph = parent.width(), parent.height()

        shw, shh = popup.sizeHint().width(), popup.sizeHint().height()

        x = px + pw - xgap - shw

        if not self.popups:
            y = py + ph - ygap - shh
        else:
            y = self.popups[-1].y() - ygap - shh

        self.popups.append(popup)

        popup.move(x, y)

        if x > parent.x() and y > parent.y():

            effect = QGraphicsOpacityEffect()
            animation = QPropertyAnimation(effect, b'opacity')

            animation.setDuration(10000)
            animation.setEasingCurve(QEasingCurve.OutExpo)
            animation.setStartValue(0.0)
            animation.setEndValue(1.0)

            self.effects[popup] = effect
            self.animations[popup] = animation

            popup.setGraphicsEffect(effect)
            # popup.label.setGraphicsEffect(effect)
            # popup.undo_btn.setGraphicsEffect(effect)
            # popup.close_btn.setGraphicsEffect(effect)
            popup.setStyleSheet('background-color: #8F0000')
            popup.show()

            animation.start() # maybe start before show?
        else:
            # there are too many popups displayed right now
            pass

        self.logger.debug(f'coordinates after move: {(popup.x(), popup.y())}')

    def delist(self, popup: QWidget) -> None:

        index = self.popups.index(popup)

        # TODO: maybe the order is important
        del self.effects[popup]
        del self.animations[popup]

        self.popups.pop(index)

        while index != len(self.popups):
            # update coordinates of subsequent popups
            index += 1

    @pyqtSlot(TResponse)
    def handle_popup(self, response: TResponse) -> None:

        if isinstance(response, TUndoResponse):
            return self.handle_popup_undo(response)
        if isinstance(response, TCloseResponse):
            return self.handle_popup_close(response)

        raise RuntimeError(f'Unknown response: {response}')

    def handle_popup_undo(self, response: TUndoResponse) -> None:

        self.delist(response.wgt)

    def handle_popup_close(self, response: TCloseResponse) -> None:

        self.delist(response.wgt)


class TCentralWidget(QWidget):

    requested = pyqtSignal(TRequest)

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.logger = logging.getLogger('poc')

        self.some_lbl = QLabel('Hello, animations!')
        self.popup_btn = QPushButton('Click for a popup')
        self.popup_clicks = 0

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.popup_btn)
        self.layout.addWidget(self.some_lbl)
        self.setLayout(self.layout)

        self.popup_btn.clicked.connect(self.handle_popup_clicked)

    @pyqtSlot()
    def handle_popup_clicked(self):
        self.requested.emit(
            TSideRequest(str('Popup ' + str(self.popup_clicks)))
        )
        self.popup_clicks += 1

    @logged(disabled=True)
    def showEvent(self, event: QShowEvent) -> None:

        super().showEvent(event)

    @logged(disabled=True)
    def hideEvent(self, event: QHideEvent) -> None:

        super().hideEvent(event)

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


class TMainWindow(QMainWindow):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.logger = logging.getLogger('poc')

        self.total_popups = 0
        self.popup_service = TPopupService(self)

        self.central_widget = TCentralWidget(self)
        self.setCentralWidget(self.central_widget)

        self.central_widget.requested.connect(self.handle_central_widget_requested)

    @pyqtSlot(TRequest)
    def handle_central_widget_requested(self, request: TRequest) -> None:

        if isinstance(request, TSideRequest):
            return self.handle_central_widget_side_request(request)

        raise RuntimeError('Unknown request from central widget')

    def handle_central_widget_side_request(self, request: TSideRequest) -> None:

        self.popup_service.notify(request.payload)

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
