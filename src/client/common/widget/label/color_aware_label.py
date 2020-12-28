from PyQt5.QtWidgets import QLabel

from src.client.common.widget.common.color_aware_widget import TColorAwareWidget  # NOQA
from src.client.common.widget.common.color_aware_widget import TColorAwareWidgetFailure  # NOQA
from src.client.common.widget.common.color_aware_widget import TColorAwareWidgetMain  # NOQA
from src.client.common.widget.common.color_aware_widget import TColorAwareWidgetNext  # NOQA
from src.client.common.widget.common.color_aware_widget import TColorAwareWidgetSuccess  # NOQA


class TColorAwareLabel(QLabel, TColorAwareWidget):
    pass


class TPrimaryColorAwareLabel(QLabel, TColorAwareWidgetMain):
    pass


class TAlternateColorAwareLabel(QLabel, TColorAwareWidgetNext):
    pass


class TSuccessColorAwareLabel(QLabel, TColorAwareWidgetSuccess):
    pass


class TFailureColorAwareLabel(QLabel, TColorAwareWidgetFailure):
    pass
