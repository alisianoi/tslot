#!/usr/bin/env python

import logging
import logging.config
import sys
import time
from functools import wraps

from PyQt5.QtCore import (QObject, QPoint, QRect, QSize, Qt, QTimer,
                          pyqtSignal, pyqtSlot)
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


class TSideWidget(QWidget):

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

        super().paintEvent(event)

        self.logger.debug(f'event.rect(): {event.rect()}')

    @logged(disabled=True)
    def closeEvent(self, event: QCloseEvent) -> None:

        super().closeEvent(event)

        self.logger.debug(f'closeEvent(): {event.spontaneous()}')

    @logged(disabled=False)
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


class TSideService(QObject):

    def __init__(self, gap: int=10):

        super().__init__()

        self.logger = logging.getLogger('poc')

        self.gap = gap
        self.active = {}

    @logged(disabled=False)
    def notify(self, parent: QWidget, txt: str) -> None:

        if parent not in self.active:
            self.active[parent] = []

        self.logger.debug(f'parent.size: {parent.size()}')
        self.logger.debug(f'parent.sizeHint: {parent.sizeHint()}')
        self.logger.debug(f'parent.geometry: {parent.geometry()}')
        self.logger.debug(f'parent.frameGeometry: {parent.frameGeometry()}')
        self.logger.debug(f'parent.normalGeometry: {parent.normalGeometry()}')

        widget = TSideWidget(txt, parent)
        widget.setStyleSheet('background-color: #008B00')
        widget.responded.connect(self.handle_side_widget)

        self.logger.debug(f'widget.size: {widget.size()}')
        self.logger.debug(f'widget.sizeHint: {widget.sizeHint()}')
        self.logger.debug(f'widget.geometry: {widget.geometry()}')
        self.logger.debug(f'widget.frameGeometry: {widget.frameGeometry()}')
        self.logger.debug(f'widget.normalGeometry: {widget.normalGeometry()}')

        self.active[parent].append(widget)

        self.move_widget(widget)

        widget.show()

        self.logger.debug(f'widget.size: {widget.size()}')
        self.logger.debug(f'widget.sizeHint: {widget.sizeHint()}')
        self.logger.debug(f'widget.geometry: {widget.geometry()}')
        self.logger.debug(f'widget.frameGeometry: {widget.frameGeometry()}')
        self.logger.debug(f'widget.normalGeometry: {widget.normalGeometry()}')


    @pyqtSlot(TResponse)
    def handle_side_widget(self, response: TResponse) -> None:

        if isinstance(response, TUndoResponse):
            return self.handle_side_widget_undo(response)
        if isinstance(response, TCloseResponse):
            return self.handle_side_widget_close(response)

        raise RuntimeError(f'Unknown response: {response}')

    def handle_side_widget_undo(self, response: TUndoResponse) -> None:

        self.unregister_widget(response)

    def handle_side_widget_close(self, response: TCloseResponse) -> None:

        self.unregister_widget(response)

    def unregister_widget(self, response: TResponse) -> None:
        widget, parent = response.wgt, response.wgt.parent()

        self.active[parent].pop(self.find_index(widget))

    def move_widget(self, widget) -> None:
        parent = widget.parent()

        wpg, wsh = parent.geometry(), widget.sizeHint()

        x = wpg.x() + wpg.width() - wsh.width() - self.gap
        y = wpg.y() + wpg.height() - wsh.height() - self.gap

        for w in self.active[parent]:
            if w is widget:
                break

            y = y - w.height() - self.gap

        widget.move(x, y)

    def find_index(self, widget: QWidget) -> int:
        for i, w in enumerate(self.active[widget.parent()]):
            if w is widget:
                return i

        raise RuntimeError('This notification widget has disappeared')


class TCentralWidget(QWidget):

    requested = pyqtSignal(TRequest)

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.logger = logging.getLogger('poc')

        self.popup_btn = QPushButton('Click for a popup')
        self.popup_clicks = 0

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.popup_btn)
        self.setLayout(self.layout)

        self.setStyleSheet('background-color: #8B0000')

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
        self.popup_service = TSideService()

        self.central_widget = TCentralWidget(self)
        self.setCentralWidget(self.central_widget)

        self.setStyleSheet('background-color: #00008B')

        self.central_widget.requested.connect(self.handle_central_widget_requested)

    @pyqtSlot(TRequest)
    def handle_central_widget_requested(self, request: TRequest) -> None:

        if isinstance(request, TSideRequest):
            return self.handle_central_widget_side_request(request)

        raise RuntimeError('Unknown request from central widget')

    def handle_central_widget_side_request(self, request: TSideRequest) -> None:

        self.popup_service.notify(self, request.payload)

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
