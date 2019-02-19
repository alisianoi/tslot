from PyQt5.QtWidgets import QHBoxLayout, QWidget

from src.client.common.widget.label.color_aware_label import *


class TLabelDemo(QWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.wgt_primary_color_aware_label = TPrimaryColorAwareLabel()
        self.wgt_alternate_color_aware_label = TAlternateColorAwareLabel()
        self.wgt_success_color_aware_label = TSuccessColorAwareLabel()
        self.wgt_failure_color_aware_label = TFailureColorAwareLabel()

        self.layout = QHBoxLayout()
        for attr in dir(self):
            if attr.startswith('wgt') and attr.endswith('label'):
                self.layout.addWidget(getattr(self, attr))
        self.setLayout(self.layout)
