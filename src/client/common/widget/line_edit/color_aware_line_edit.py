from PyQt5.QtWidgets import QLineEdit

from src.client.common.widget.common.color_aware_widget import *


class TColorAwareLineEdit(QLineEdit, TColorAwareWidget):

    pass


class TPrimaryColorAwareLineEdit(QLineEdit, TPrimaryColorAwareWidget):

    pass


class TAlternateColorAwareLineEdit(QLineEdit, TAlternateColorAwareWidget):

    pass


class TSuccessColorAwareLineEdit(QLineEdit, TSuccessColorAwareWidget):

    pass


class TFailureColorAwareLineEdit(QLineEdit, TFailureColorAwareWidget):

    pass
