from PyQt5.QtCore import Qt, pyqtSlot

from src.client.common.widget.scroll_area import TScrollArea
from src.client.wgt_timer_table.widget.scroll_widget import TScrollWidget


class THomeScrollArea(TScrollArea):
    """Show several tables that contain time slots"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setWidget(TScrollWidget())
        self.setWidgetResizable(True)

    @pyqtSlot()
    def handle_show_next_shortcut(self):
        self.widget().request_next()
