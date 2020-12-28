from PyQt5.QtWidgets import QPushButton

from src.client.common.widget.common.color_aware_widget import *


class TColorAwarePushButton(QPushButton, TColorAwareWidget):

    pass


class TPrimaryColorAwarePushButton(QPushButton, TColorAwareWidgetMain):

    pass


class TAlternateColorAwarePushButton(QPushButton, TColorAwareWidgetNext):

    pass


class TSuccessColorAwarePushButton(QPushButton, TColorAwareWidgetSuccess):

    pass


class TFailureColorAwarePushButton(QPushButton, TColorAwareWidgetFailure):

    pass
