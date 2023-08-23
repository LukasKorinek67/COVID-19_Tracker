from PyQt5.QtWidgets import QTabWidget
from CasesTab import CasesTab
from VaccTab import VaccTab


class TabsWidget(QTabWidget):
    def __init__(self, *args, **kwargs):
        super(QTabWidget, self).__init__(*args, **kwargs)
        self.cases_tab = CasesTab()
        self.vacc_tab = VaccTab()
        self.addTab(self.cases_tab, 'Nové případy')
        self.addTab(self.vacc_tab, 'Očkování')
