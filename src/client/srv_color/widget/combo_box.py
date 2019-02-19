import re

from PyQt5.QtWidgets import QWidget

from src.client.common.widget.combo_box import TComboBox
from src.client.srv_color.service.color import TColorService


class MyComboBox(TComboBox):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.colors = TColorService()
        self.addItems([clr for clr in dir(self.colors) if self.colors.is_color_attr(clr)])
