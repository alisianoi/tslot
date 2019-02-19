from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QWidget

from common.widget.combo_box import EditableComboBox


class TFontComboBox(EditableComboBox):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.setItemsAndData([
            ("Serif", "font_serif")
            , ("Sans Serif", "font_sans_serif")
            , ("Monospace", "font_monospace")
        ])


class TFontFamilyComboBox(EditableComboBox):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.addItems([family for family in QFontDatabase().families()])


class TFontStyleComboBox(EditableComboBox):

    pass
