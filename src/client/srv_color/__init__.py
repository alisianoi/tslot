import re

from PyQt5.QtWidgets import *

from src.common.logger import logged, logmain
from src.client.srv_color.service.color import TColorService
from src.client.srv_color.widget.combo_box import MyComboBox
from src.client.srv_color.widget.label import MyLabel
from src.client.srv_color.widget.line_edit import MyLineEdit
from src.client.srv_color.widget.push_button import MyPushButton
from src.client.srv_color.widget.spin_box import MySpinBox


class TColorSettings(QWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create widgets
        self.widget_0 = MyLabel("Color")
        self.widget_1 = MyComboBox()
        self.widget_2 = MyLineEdit()
        self.widget_3 = MySpinBox()
        self.widget_4 = MyPushButton("Tell size")

        # Connect signals
        ## Handle signals from the color names combo box dropdown
        self.widget_1.activated.connect(self.handle_combo_box_activated)
        self.widget_1.currentIndexChanged.connect(self.handle_combo_box_current_index_changed)
        self.widget_1.highlighted.connect(self.handle_combo_box_highlighted)
        ## Handle signals from the color values line edit
        self.widget_2.cursorPositionChanged.connect(self.handle_line_edit_cursor_position_changed)
        self.widget_2.editingFinished.connect(self.handle_line_edit_editing_finished)
        # self.widget_2.inputRejected.connect(self.handle_line_edit_input_rejected)
        self.widget_2.returnPressed.connect(self.handle_line_edit_return_pressed)
        self.widget_2.selectionChanged.connect(self.handle_line_edit_selection_changed)
        self.widget_2.textChanged.connect(self.handle_line_edit_text_changed)
        self.widget_2.textEdited.connect(self.handle_line_edit_text_edited)
        ## Handles signals from the push button
        self.widget_4.clicked.connect(self.handle_clicked)

        # Initialize widgets
        chosen_color_key = self.widget_1.currentText()
        self.widget_2.setText(getattr(MyColorService(), chosen_color_key))

        # Add widgets to layout
        pattern = re.compile("^widget_[0-9]+$")
        self.layout_0 = QHBoxLayout()
        for attr in dir(self):
            if pattern.match(attr):
                self.layout_0.addWidget(getattr(self, attr))
        self.layout_0.addStretch(10)
        self.setLayout(self.layout_0)

    def handle_clicked(self):
        logmain.debug(f'Here are MyStyleSettings({self.height()}, {self.width()})')
        logmain.debug(f'Here is the MyLabel({self.widget_0.height()}, {self.widget_0.width()})')
        logmain.debug(f'Here is the MyComboBox({self.widget_1.height()}, {self.widget_1.width()})')
        logmain.debug(f'Here is the MyLineEdit({self.widget_2.height()}, {self.widget_2.width()})')
        logmain.debug(f'Here is the QSpinBox({self.widget_3.height()}, {self.widget_3.width()})')
        logmain.debug(f'Here is the MyPushButton({self.widget_4.height()}, {self.widget_4.width()})')

    def handle_combo_box_activated(self, index):
        chosen_color_key = self.widget_1.currentText()
        self.widget_2.setText(getattr(MyColorService(), chosen_color_key))

    def handle_combo_box_current_index_changed(self, index):
        # logmain.debug(f'The index is {index}')
        pass

    def handle_combo_box_highlighted(self, index):
        # logmain.debug(f'The index is {index}')
        pass

    @logged(disabled=True)
    def handle_line_edit_cursor_position_changed(self, old_position: int, new_position: int):
        pass

    @logged(disabled=True)
    def handle_line_edit_editing_finished(self):
        chosen_color_key = self.widget_1.currentText()
        chosen_color_val = self.widget_2.text()

        setattr(MyColorService(), chosen_color_key, chosen_color_val)

    @logged(disabled=True)
    def handle_line_edit_input_rejected(self):
        pass

    @logged(disabled=True)
    def handle_line_edit_return_pressed(self):
        self.widget_2.clearFocus()

    @logged(disabled=True)
    def handle_line_edit_selection_changed(self):
        pass

    @logged(disabled=True)
    def handle_line_edit_text_changed(self, text):
        pass

    @logged(disabled=True)
    def handle_line_edit_text_edited(self, text):
        pass
