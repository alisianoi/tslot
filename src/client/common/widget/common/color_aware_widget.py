from PyQt5.QtWidgets import QWidget

from src.client.srv_color.service.color import TColorService


class TColorAwareWidget(QWidget):
    """Base class for all color aware widgets."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._color_service = TColorService()

    def set_style_sheet(self, class_name: str, fg_color: str, bg_color: str):
        self.setStyleSheet(f"""
            {class_name} {{
                color: {fg_color};
                background-color: {bg_color};
            }}"""
        )


class TColorAwareWidgetMain(TColorAwareWidget):
    """Color aware widget: primary colors used"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._color_service.fg_color_fst_lgt_changed.connect(
            self._handle_style_sheet_changed
        )
        self._color_service.bg_color_fst_lgt_changed.connect(
            self._handle_style_sheet_changed
        )

        self._handle_style_sheet_changed()

    def _handle_style_sheet_changed(self):
        self.set_style_sheet(
            self.__class__.__name__
            , self._color_service.fg_color_fst_lgt
            , self._color_service.bg_color_fst_lgt
        )


class TColorAwareWidgetNext(TColorAwareWidget):
    """Color aware widget: secondary colors used"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._color_service.fg_color_snd_lgt_changed.connect(
            self._handle_style_sheet_changed
        )
        self._color_service.bg_color_snd_lgt_changed.connect(
            self._handle_style_sheet_changed
        )

        self._handle_style_sheet_changed()

    def _handle_style_sheet_changed(self):
        self.set_style_sheet(
            self.__class__.__name__
            , self._color_service.fg_color_snd_lgt
            , self._color_service.bg_color_snd_lgt
        )


class TColorAwareWidgetSuccess(TColorAwareWidgetNext):
    """Color aware widget: colors indicate positive outcome"""
    pass


class TColorAwareWidgetFailure(TColorAwareWidget):
    """Color aware widget: colors indicate negative outcome"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._color_service.fg_color_err_changed.connect(
            self._handle_style_sheet_changed
        )
        self._color_service.bg_color_err_changed.connect(
            self._handle_style_sheet_changed
        )

        self._handle_style_sheet_changed()

    def _handle_style_sheet_changed(self):
        self.set_style_sheet(
            self.__class__.__name__
            , self._color_service.fg_color_err
            , self._color_service.bg_color_err
        )
