from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget


class TFontTreeWidget(QTreeWidget):

    def __init__(self, parent: QWidget = None):

        super().__init__(parent)

        self.font_database = QFontDatabase()

        self.setColumnCount(2)
        self.setHeaderLabels(["Font", "Smooth Sizes"])

        for family in self.font_database.families():
            font_family_item = QTreeWidgetItem(self)
            font_family_item.setText(0, family)

            for style in self.font_database.styles(family):
                font_style_item = QTreeWidgetItem(font_family_item)
                font_style_item.setText(0, style)

                sizes = ''
                for size in self.font_database.smoothSizes(family, style):
                    sizes += str(size) + ' '

                font_style_item.setText(1, sizes)
