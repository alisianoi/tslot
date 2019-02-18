from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QLabel, QSizePolicy

from logger import logged, logger
from srv_color.service.color import MyColorService
from srv_font.service.font import MyFontService


class StyledLabel(QLabel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.font_service = MyFontService()
        self.color_service = MyColorService()

        self.font_service.base_height_changed.connect(
            self.handle_base_height_changed
        )
        self.font_service.font_sans_serif_changed.connect(
            self.handle_font_sans_serif_changed
        )

        self.setFont(self.font_service.font_sans_serif)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

    def handle_base_height_changed(self):
        self.updateGeometry()

    def handle_font_sans_serif_changed(self):
        self.setFont(self.font_service.font_sans_serif)
        self.updateGeometry()

    def set_style_sheet(self, class_name: str, fg_color: str, bg_color: str) -> None:
        self.setStyleSheet(f"""
            {class_name} {{
                color: {fg_color};
                background-color: {bg_color};
            }}"""
        )

    @logged(disabled=True)
    def sizeHint(self) -> QSize:
        size_hint = super().sizeHint()
        return QSize(size_hint.width(), self.font_service.base_height)

    @logged(disabled=True)
    def minimumSizeHint(self) -> QSize:
        size_hint = super().sizeHint()
        return QSize(size_hint.width(), self.font_service.base_height)

    @logged(disabled=True)
    def maximumSizeHint(self) -> QSize:
        size_hint = super().maximumSizeHint()
        return QSize(size_hint.width(), self.font_service.base_height)


class PrimaryLabel(StyledLabel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.handle_style_sheet_changed()

        self.color_service.fg_color_fst_lgt_changed.connect(self.handle_style_sheet_changed)
        self.color_service.bg_color_fst_lgt_changed.connect(self.handle_style_sheet_changed)

    def handle_style_sheet_changed(self):
        self.set_style_sheet(
            self.__class__.__name__
            , self.color_service.fg_color_fst_lgt
            , self.color_service.bg_color_fst_lgt
        )


class AlternateLabel(StyledLabel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.handle_style_sheet_changed()

        self.color_service.fg_color_snd_lgt_changed.connect(self.handle_style_sheet_changed)
        self.color_service.bg_color_snd_lgt_changed.connect(self.handle_style_sheet_changed)

    def handle_style_sheet_changed(self):
        self.set_style_sheet(
            self.__class__.__name__
            , self.color_service.fg_color_snd_lgt
            , self.color_service.bg_color_snd_lgt
        )


class SuccessLabel(AlternateLabel):

    pass


class FailureLabel(StyledLabel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.handle_style_sheet_changed()

        self.color_service.fg_color_err_changed.connect(self.handle_style_sheet_changed)
        self.color_service.bg_color_err_changed.connect(self.handle_style_sheet_changed)

    def handle_style_sheet_changed(self):
        self.set_style_sheet(
            self.__class__.__name__
            , self.color_service.fg_color_err
            , self.color_service.bg_color_err
        )
