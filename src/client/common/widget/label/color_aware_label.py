from PyQt5.QtWidgets import QLabel

from src.client.common.widget.common.color_aware_widget import *


class TColorAwareLabel(QLabel, TColorAwareWidget):

    pass


class TPrimaryColorAwareLabel(QLabel, TPrimaryColorAwareWidget):

    pass


class TAlternateColorAwareLabel(QLabel, TAlternateColorAwareWidget):

    pass


class TSuccessColorAwareLabel(QLabel, TSuccessColorAwareWidget):

    pass


class TFailureColorAwareLabel(QLabel, TFailureColorAwareWidget):

    pass
