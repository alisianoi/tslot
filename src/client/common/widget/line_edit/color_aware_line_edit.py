from PyQt5.QtWidgets import QLineEdit

from src.client.common.widget.common.color_aware_widget import *


class TColorAwareLineEdit(QLineEdit, TColorAwareWidget):

    pass


class TPrimaryColorAwareLineEdit(QLineEdit, TColorAwareWidgetMain):

    pass


class TAlternateColorAwareLineEdit(QLineEdit, TColorAwareWidgetNext):

    pass


class TSuccessColorAwareLineEdit(QLineEdit, TColorAwareWidgetSuccess):

    pass


class TFailureColorAwareLineEdit(QLineEdit, TColorAwareWidgetFailure):

    pass
