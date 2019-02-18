from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QWidget

from common.widget.combo_box import EditableComboBox


class MyFontComboBox(EditableComboBox):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.setItemsAndData([
            ("Serif", "font_serif")
            , ("Sans Serif", "font_sans_serif")
            , ("Monospace", "font_monospace")
        ])


class MyFontFamilyComboBox(EditableComboBox):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.addItems([family for family in QFontDatabase().families()])


class MyFontStyleComboBox(EditableComboBox):

    pass
