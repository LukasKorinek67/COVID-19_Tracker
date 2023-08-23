from PyQt5.QtCore import QObject, pyqtSignal, QTime
import time


class AutoUpdater(QObject):
    update = pyqtSignal()

    def __init__(self, interval):
        super().__init__()
        #self.time_window = (QTime(8, 0, 0, 0), QTime(9, 0, 0, 0))
        self.interval = interval * 60

    def run(self):
        while True:
            """
            now = QTime.currentTime()
            if self.time_window[0] <= now < self.time_window[1]:
                self.update.emit()
            """
            self.update.emit()
            time.sleep(self.interval)
