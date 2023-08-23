import PyQt5.QtWidgets as qw
from PyQt5.QtCore import Qt, QPropertyAnimation, QThread
from QuickSearch import QuickSearch
from PyQt5 import QtGui
from BarGraph import BarGraph
import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

from Controller import Controller
from VaccUpdateThread import VaccUpdateThread
from AutoUpdater import AutoUpdater


class VaccTab(qw.QWidget):
    def __init__(self, *args, **kwargs):
        super(VaccTab, self).__init__(*args, **kwargs)
        # VLAKNA
         # auto update vlakno
        self.auto_update_thread = QThread()
        self.auto_update = AutoUpdater(interval=15)
        self.auto_update.moveToThread(self.auto_update_thread)
        self.auto_update_thread.started.connect(self.auto_update.run)
        self.auto_update.update.connect(self.update_fun)
            # update vlakno
        self.update_thread = QThread()
        self.update = VaccUpdateThread()
        self.update.moveToThread(self.update_thread)
        self.update_thread.started.connect(self.update.update_data)
        self.update.finished.connect(self.update_states)
        self.update.finished.connect(self.update_thread.quit)

        self.container = qw.QVBoxLayout()
        self.title = qw.QLabel('Přehled očkování COVID-19')
        self.title.setStyleSheet(open(get_full_path('styles.css')).read())
        self.updated_label = qw.QLabel('Aktualizováno')
        self.hide(self.updated_label)
        self.updated_label.setStyleSheet('margin-right:3px; margin-bottom:10px;')
        self.title_bttn_layout = qw.QHBoxLayout()
        self.update_bttn = qw.QPushButton('Aktualizovat data')
        self.update_bttn.setStyleSheet(open(get_full_path('styles.css')).read())
        # - tady jsem přidal po kliknutí na "Aktualizovat data" provedení metody update_data()
        self.update_bttn.clicked.connect(self.update_fun)
        self.title_bttn_layout.addWidget(self.title, 10)
        self.title_bttn_layout.addWidget(self.updated_label, 1)
        self.title_bttn_layout.addWidget(self.update_bttn, 1)
        self.title_bttn_layout.setAlignment(self.updated_label, Qt.AlignRight)

        self.countries = [["", 0],
                          ["", 0],
                          ["", 0],
                          ["", 0],
                          ["", 0]]

        # QUICKSEARCHE A GRAF
        self.search_graph_widget = qw.QWidget()
        self.search_graph_layout = qw.QHBoxLayout(self.search_graph_widget)
        #    Quicksearche
        self.quicksearch_frame = qw.QFrame()
        self.quicksearch_frame.setLineWidth(1)
        self.quicksearch_frame.setFrameStyle(qw.QFrame.Box | qw.QFrame.Plain)
        self.quicksearch_layout = qw.QVBoxLayout(self.quicksearch_frame)
        self.quicksearch_label = qw.QLabel('Vybrané země k porovnání')
        self.quicksearch_label.setStyleSheet('font-size: 16px; font-family: Arial; margin-top:10px;')
        self.sep_line = qw.QFrame()
        self.sep_line.setFrameShape(qw.QFrame.HLine)
        self.sep_line.setSizePolicy(qw.QSizePolicy.Expanding,
                                    qw.QSizePolicy.Minimum)
        self.quicksearch1 = QuickSearch()
        self.quicksearch1.set_default_text('Czechia')
        self.quicksearch1.search_bttn.clicked.connect(self.update_view)
        self.quicksearch2 = QuickSearch()
        self.quicksearch2.search_bttn.clicked.connect(self.update_view)
        self.quicksearch3 = QuickSearch()
        self.quicksearch3.search_bttn.clicked.connect(self.update_view)
        self.quicksearch4 = QuickSearch()
        self.quicksearch4.search_bttn.clicked.connect(self.update_view)
        self.quicksearch5 = QuickSearch()
        self.quicksearch5.search_bttn.clicked.connect(self.update_view)
        self.quicksearch_layout.addWidget(self.quicksearch_label)
        self.quicksearch_layout.addWidget(self.sep_line)
        self.quicksearch_layout.addWidget(self.quicksearch1)
        self.quicksearch_layout.addWidget(self.quicksearch2)
        self.quicksearch_layout.addWidget(self.quicksearch3)
        self.quicksearch_layout.addWidget(self.quicksearch4)
        self.quicksearch_layout.addWidget(self.quicksearch5)
        self.quicksearch_layout.setAlignment(self.quicksearch_label,
                                             Qt.AlignCenter)
        #    Graf
        self.graph_frame = qw.QFrame()
        self.graph_frame.setLineWidth(1)
        self.graph_frame.setFrameStyle(qw.QFrame.Box | qw.QFrame.Plain)
        self.graph_layout = qw.QVBoxLayout(self.graph_frame)
        self.graph = BarGraph()
        self.graph_layout.addWidget(self.graph)
        self.graph_layout.setAlignment(self.graph, Qt.AlignCenter)

        # TABULKA
        self.table_title = qw.QLabel('Vybrané země (proočkování obyvatel v %), poslední dostupná data')
        self.table_title.setStyleSheet('font-size: 16px; font-family: Arial;')
        self.table = qw.QTableWidget()
        self.table.setColumnCount(6)
        self.table.setRowCount(20)
        self.table.setHorizontalHeaderLabels(['Datum aktualizace', 'Zeme1', 'Zeme2',
                                              'Zeme3', 'Zeme4', 'Zeme5'])
        self.table.verticalHeader().setVisible(False)
        self.table.setMinimumWidth(790)
        palette = self.table.palette()
        palette.setBrush(QtGui.QPalette.Highlight, QtGui.QBrush(Qt.white))
        palette.setBrush(QtGui.QPalette.HighlightedText,
                         QtGui.QBrush(Qt.black))
        self.table.setPalette(palette)
        self.table.setEditTriggers(qw.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(qw.QAbstractItemView.NoSelection)
        self.table.horizontalHeader().setSectionResizeMode(qw.QHeaderView.Stretch)
        self.table.horizontalHeader().setStyleSheet(open(get_full_path('styles.css')).read())

        self.search_graph_layout.addWidget(self.quicksearch_frame, 1)
        self.search_graph_layout.addWidget(self.graph_frame, 2)
        self.container.addLayout(self.title_bttn_layout, 1)
        self.container.addWidget(self.search_graph_widget, 4)
        self.container.addWidget(self.table_title, 1)
        self.container.setAlignment(self.table_title, Qt.AlignCenter)
        self.container.addWidget(self.table, 3)
        self.container.setSpacing(0)
        self.setLayout(self.container)

        #pro počáteční zobrazení dat ČR
        #self.add_rows()
        self.auto_update_thread.start()
        #self.update_states()

    def update_view(self):
        """
        - zavolat tady funkci set_state_not_chosen() s argumentem jména státu kterej
        př.
        Na státu 2 byla vybraná Čína
        Uživatel přepsal Čínu na Japonsko, protože chce data Japonska
        Zavolat set_state_not_chosen("China")
        Pak už udělat get_state_vaccination_data("Japan", number) a přepsat data v grafu a tabulce
        - number je pořadí toho statů jak jsme se bavili
        """
        self.update_states()
        
        """
        Tohle jsi tu měl předtím:
        self.countries = [(self.quicksearch1.text(), 65),
                     (self.quicksearch2.text(), 20),
                     (self.quicksearch3.text(), 35),
                     (self.quicksearch4.text(), 45),
                     (self.quicksearch5.text(), 10)]
        self.graph.update(self.countries)
        self.table.setHorizontalHeaderLabels(['Datum aktualizace',
                                              self.countries[0][0],
                                              self.countries[1][0],
                                              self.countries[2][0],
                                              self.countries[3][0],
                                              self.countries[4][0]])
        """


    def update_states(self):
        controller = Controller()
        quicksearches = [self.quicksearch1, self.quicksearch2, self.quicksearch3,
                         self.quicksearch4, self.quicksearch5]
        for (i, qs) in enumerate(quicksearches):
            controller.set_state_not_chosen(self.countries[i][0])
            controller.set_state_chosen(qs.text(), i+1)
        self.add_rows()
        self.update_bttn.setEnabled(True)
        self.quicksearch1.search_bttn.setEnabled(True)
        self.quicksearch2.search_bttn.setEnabled(True)
        self.quicksearch3.search_bttn.setEnabled(True)
        self.quicksearch4.search_bttn.setEnabled(True)
        self.quicksearch5.search_bttn.setEnabled(True)
        self.updated_label.setText('Aktualizováno')
        self.unfade(self.updated_label)
        self.fade(self.updated_label)
        
        """
        state_one = controller.get_state_vaccination_data(self.quicksearch1.text(), 1)
        if state_one is not None:
            state_one_last_data = state_one.data[-1]
            state_one_percentage = state_one_last_data["percentage"]
            self.countries[0][0] = state_one.state
            self.countries[0][1] = float(state_one_percentage)

        state_two = controller.get_state_vaccination_data(self.quicksearch2.text(), 2)
        if state_two is not None:
            state_two_last_data = state_two.data[-1]
            state_two_percentage = state_two_last_data["percentage"]
            self.countries[1][0] = state_two.state
            self.countries[1][1] = float(state_two_percentage)

        state_three = controller.get_state_vaccination_data(self.quicksearch3.text(), 3)
        if state_three is not None:
            state_three_last_data = state_three.data[-1]
            state_three_percentage = state_three_last_data["percentage"]
            self.countries[2][0] = state_three.state
            self.countries[2][1] = float(state_three_percentage)

        state_four = controller.get_state_vaccination_data(self.quicksearch4.text(), 4)
        if state_four is not None:
            state_four_last_data = state_four.data[-1]
            state_four_percentage = state_four_last_data["percentage"]
            self.countries[3][0] = state_four.state
            self.countries[3][1] = float(state_four_percentage)

        state_five = controller.get_state_vaccination_data(self.quicksearch5.text(), 5)
        if state_five is not None:
            state_five_last_data = state_five.data[-1]
            state_five_percentage = state_five_last_data["percentage"]
            self.countries[4][0] = state_five.state
            self.countries[4][1] = float(state_five_percentage)

        self.graph.update(self.countries)
        self.table.setHorizontalHeaderLabels(['Datum aktualizace',
                                              self.countries[0][0],
                                              self.countries[1][0],
                                              self.countries[2][0],
                                              self.countries[3][0],
                                              self.countries[4][0]])
        """
    def update_fun(self):
        self.update_thread.start()
        self.updated_label.setText('Aktualizuji...')
        self.unfade(self.updated_label)
        self.update_bttn.setEnabled(False)
        self.quicksearch1.search_bttn.setEnabled(False)
        self.quicksearch2.search_bttn.setEnabled(False)
        self.quicksearch3.search_bttn.setEnabled(False)
        self.quicksearch4.search_bttn.setEnabled(False)
        self.quicksearch5.search_bttn.setEnabled(False)

    def update_data(self):
        #controller = Controller()
        #controller.update_vaccination_data()
        self.update_states()

    def hide(self, widget):
        self.effect = qw.QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)
        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(1)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

    def fade(self, widget):
        self.effect = qw.QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)
        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(1000)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

    def unfade(self, widget):
        self.effect = qw.QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)
        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(1000)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    def add_rows(self):
        rows = self.get_rows()
        # Vymažu starý data a dám tam nový
        for i in reversed(range(self.table.rowCount())):
            self.table.removeRow(i)
        #
        for row in rows:
            self.table.insertRow(0)
            for i, col in enumerate(row):
                item = qw.QTableWidgetItem(col)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(0, i, item)
        self.unfade(self.updated_label)
        self.fade(self.updated_label)
        self.update_bttn.setEnabled(True)

    def get_rows(self):
        self.countries = [["", 0],
                          ["", 0],
                          ["", 0],
                          ["", 0],
                          ["", 0]]
        controller = Controller()
        data = controller.get_vaccination_data()
        rows = [["" for i in range(6)] for j in range(len(data[0].data))]
        qs = [self.quicksearch1, self.quicksearch2, self.quicksearch3,
              self.quicksearch4, self.quicksearch5]
        for state in data:
            column_num = state.is_chosen
            last_percentage = state.data[-1]['percentage']
            if last_percentage != "":
                self.countries[column_num-1] = [state.state, float(last_percentage)]
            else:
                self.countries[column_num-1] = [state.state, 0]
            qs[column_num-1].set_default_text(state.state)
            for (i, day) in enumerate(state.data):
                #rows[i][column_num] = day['percentage']
                percentage = day['percentage']
                if percentage == "":
                    rows[i][column_num] = "Data nezveřejněna"
                else:
                    percentage = percentage.replace(".", ",")
                    rows[i][column_num] = percentage + "%"
                date = day['date']
                czech_date = date[8:10] + "." + date[5:7] + "." + date[0:4]
                rows[i][0] = czech_date
        self.graph.update(self.countries)
        self.table.setHorizontalHeaderLabels(['Datum aktualizace',
                                              self.countries[0][0],
                                              self.countries[1][0],
                                              self.countries[2][0],
                                              self.countries[3][0],
                                              self.countries[4][0]])
        return rows


def get_full_path(file_name):
    """
    Funkce pro získání celé cesty k souboru - vrací celé jméno souboru i s cestou
    """
    file_location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    return os.path.join(file_location, file_name)
