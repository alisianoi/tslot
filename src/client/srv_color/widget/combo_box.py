import re

from PyQt5.QtWidgets import QWidget

from common.widget.combo_box import ComboBox
from srv_color.service.color import MyColorService


class MyComboBox(ComboBox):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.colors = MyColorService()
        self.addItems([clr for clr in dir(self.colors) if self.colors.is_color_attr(clr)])
