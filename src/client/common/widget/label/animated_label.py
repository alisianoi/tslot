from PyQt5.QtCore import *
from PyQt5.QtGui import QHideEvent, QShowEvent
from PyQt5.QtWidgets import *

from logger import logged, logger


class AnimatedLabel(QLabel):

    enter_animation_played = pyqtSignal()
    leave_animation_played = pyqtSignal()

    def __init__(self, animate: bool = True, **kwds):
        super().__init__(**kwds)

        self.animate = animate
        self.base_animation_duration = 700

        self.enter_animation_group = QParallelAnimationGroup()
        self.leave_animation_group = QParallelAnimationGroup()

    @logged(disabled=True)
    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)

        if self.animate:
            self._play_enter_animation()

    @logged(disabled=True)
    def hideEvent(self, event: QHideEvent) -> None:
        super().hideEvent(event)

        if self.animate:
            self._play_leave_animation()

    @logged(disabled=True)
    def _play_enter_animation(self):
        self.leave_animation_group.stop()
        self.enter_animation_group.clear()

        self.enter_opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.enter_opacity_effect)

        self.enter_opacity_animation = QPropertyAnimation(
            self.enter_opacity_effect, b"opacity"
        )
        self.enter_opacity_animation.setStartValue(0.0)
        self.enter_opacity_animation.setEndValue(1.0)
        self.enter_opacity_animation.setDuration(self.base_animation_duration)

        self.enter_animation_group.addAnimation(self.enter_opacity_animation)
        self.enter_animation_group.finished.connect(
            self._handle_enter_animation_group_finished
        )

        self.enter_animation_group.start()

    @logged(disabled=True)
    def _play_leave_animation(self):
        self.enter_animation_group.stop()
        self.leave_animation_group.clear()

        self.leave_opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.leave_opacity_effect)

        self.leave_opacity_animation = QPropertyAnimation(
            self.leave_opacity_effect, b"opacity"
        )
        self.leave_opacity_animation.setStartValue(1.0)
        self.leave_opacity_animation.setEndValue(0.0)
        self.leave_opacity_animation.setDuration(self.base_animation_duration)

        # self.leave_animation_group.addAnimation(self.leave_animation_group)
        self.leave_animation_group.finished.connect(
            self._handle_leave_animation_group_finished
        )

        self.leave_animation_group.start()

    @logged(disabled=True)
    def _handle_enter_animation_group_finished(self):
        self.enter_animation_played.emit()
        super().show()

    @logged(disabled=True)
    def _handle_leave_animation_group_finished(self):
        self.leave_animation_played.emit()
        super().hide()
