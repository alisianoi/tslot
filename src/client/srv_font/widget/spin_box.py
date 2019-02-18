from PyQt5.QtWidgets import QWidget

from common.widget.spin_box import SpinBox
from logger import logged
from srv_font.service.font import MyFontService


class MySpinBox(SpinBox):

    pass


class MyFontSizeSpinBox(MySpinBox):

    pass


class MyBaseHeightSpinBox(MySpinBox):

    def __init__(self, parent: QWidget = None):

        super().__init__(parent)

        self.setValue(MyFontService().base_height)
        self.valueChanged.connect(self.handle_self_value_changed)

    def handle_self_value_changed(self):
        MyFontService().base_height = self.value()
