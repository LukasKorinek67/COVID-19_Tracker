from PyQt5.QtCore import QObject, pyqtSignal
import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

from Controller import Controller


class VaccUpdateThread(QObject):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

    def update_data(self):
        controller = Controller()
        controller.update_vaccination_data()
        self.finished.emit()
