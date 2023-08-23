from PyQt5.QtWidgets import QMainWindow
from TabsWidget import TabsWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('COVID IS')
        self.tabs_widget = TabsWidget(self)
        self.setCentralWidget(self.tabs_widget)
