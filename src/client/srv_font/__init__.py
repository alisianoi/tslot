from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtWidgets import *

from src.common.logger import logged, logmain
from src.client.common.widget.label.color_aware_label import *


class MyFontSettings(QWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.service = TFontService()

        # Create widgets
        self.wgt_font_label = TPrimaryColorAwareLabel("Font:")
        self.wgt_font_combo_box = MyFontComboBox()
        self.wgt_font_family_label = TPrimaryColorAwareLabel("Font family:")
        self.wgt_font_family_combo_box = MyFontFamilyComboBox()
        self.wgt_font_style_label = TPrimaryColorAwareLabel("Font style:")
        self.wgt_font_style_combo_box = MyFontStyleComboBox()
        self.wgt_font_size_label = TPrimaryColorAwareLabel("Font size:")
        self.wgt_font_size_spin_box = MyFontSizeSpinBox()
        self.wgt_base_size_label = TPrimaryColorAwareLabel("Base size:")
        self.wgt_base_size_spin_box = MyBaseHeightSpinBox()

        # self.wgt_font_tree_widget = FontTreeWidget()

        # Connect signals
        self.wgt_font_combo_box.currentTextChanged.connect(
            self.handle_font_combo_box_current_text_changed
        )
        self.wgt_font_family_combo_box.currentTextChanged.connect(
            self.handle_font_family_combo_box_current_text_changed
        )
        self.wgt_font_style_combo_box.currentTextChanged.connect(
            self.handle_font_style_combo_box_current_text_changed
        )
        self.wgt_font_size_spin_box.valueChanged.connect(
            self.handle_font_size_spin_box_value_changed
        )

        # Initialize widgets
        self.handle_font_combo_box_current_text_changed(self.wgt_font_combo_box.currentData())
        self.handle_font_family_combo_box_current_text_changed(self.wgt_font_family_combo_box.currentText())

        # Add widgets to layout
        self.layout = QVBoxLayout()
        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.wgt_font_label, 1, 1)
        self.grid_layout.addWidget(self.wgt_font_combo_box, 1, 2)
        self.grid_layout.addWidget(self.wgt_font_family_label, 2, 1)
        self.grid_layout.addWidget(self.wgt_font_family_combo_box, 2, 2)
        self.grid_layout.addWidget(self.wgt_font_style_label, 3, 1)
        self.grid_layout.addWidget(self.wgt_font_style_combo_box, 3, 2)
        self.grid_layout.addWidget(self.wgt_font_size_label, 4, 1)
        self.grid_layout.addWidget(self.wgt_font_size_spin_box, 4, 2)
        self.grid_layout.addWidget(self.wgt_base_size_label, 5, 1)
        self.grid_layout.addWidget(self.wgt_base_size_spin_box, 5, 2)
        self.layout.addLayout(self.grid_layout)
        # self.layout.addWidget(self.wgt_font_tree_widget)
        self.setLayout(self.layout)

    def handle_font_combo_box_current_text_changed(self, txt: str):
        font_attr = self.wgt_font_combo_box.currentData()

        self._show_font_settings(font_attr)

    def handle_font_family_combo_box_current_text_changed(self, txt: str):
        font_attr = self.wgt_font_combo_box.currentData()

        styles = [style for style in QFontDatabase().styles(txt)]

        self.wgt_font_style_combo_box.setItems(styles)

        for style in styles:
            if style.capitalize() in ["Normal", "Regular", "Roman"]:
                self.wgt_font_style_combo_box.setCurrentText(style)

        setattr(self.service, font_attr + "_name", txt)
        setattr(self.service, font_attr + "_style_name", self.wgt_font_style_combo_box.currentText())
        setattr(self.service, font_attr + "_size", self.service.font_size)

    def handle_font_style_combo_box_current_text_changed(self, txt: str):
        font_attr = self.wgt_font_combo_box.currentData()
        setattr(self.service, font_attr + "_style_name", txt)

    def handle_font_size_spin_box_value_changed(self, txt: str) -> None:
        font_attr = self.wgt_font_combo_box.currentData()
        setattr(self.service, font_attr + "_size", int(txt))

    def _show_font_settings(self, font_attr: str):
        font_name = getattr(self.service, font_attr + "_name")
        font_size = getattr(self.service, font_attr + "_size")
        font_style_name = getattr(self.service, font_attr + "_style_name")

        self.wgt_font_family_combo_box.setCurrentText(font_name)
        self.wgt_font_style_combo_box.setCurrentText(font_style_name)
        self.wgt_font_size_spin_box.setValue(font_size)
