from PyQt5.QtWidgets import QPushButton

from src.client.common.widget.common.color_aware_widget import *


class TColorAwarePushButton(QPushButton, TColorAwareWidget):

    pass


class TPrimaryColorAwarePushButton(QPushButton, TPrimaryColorAwareWidget):

    pass


class TAlternateColorAwarePushButton(QPushButton, TAlternateColorAwareWidget):

    pass


class TSuccessColorAwarePushButton(QPushButton, TSuccessColorAwareWidget):

    pass


class TFailureColorAwarePushButton(QPushButton, TFailureColorAwareWidget):

    pass
