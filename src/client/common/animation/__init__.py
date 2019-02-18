from PyQt5.QtCore import QObject, QVariant, QVariantAnimation, pyqtSlot

from logger import logger


class ProgressAnimation(QVariantAnimation):
    """Create an animated progress value and change it X times per second."""

    def __init__(self, duration: int, loop_count: int = -1, fps: int = 60, **kwargs):
        super().__init__(**kwargs)

        # Expect to be 24, 30 or 60
        self.fps = fps

        self.progress = 0

        # Expect to be milliseconds, i.e. 1 second is 1000 milliseconds
        self.setDuration(duration)
        self.setStartValue(0)
        self.setEndValue(int(duration / 1000 * fps))
        self.setLoopCount(loop_count)

        self.valueChanged.connect(self.handle_value_changed)

    def handle_value_changed(self, value: int):
        self.progress = value / self.endValue()
