import PyQt5.QtWidgets as qw
from PyQt5.QtCore import Qt, QPropertyAnimation, QThread
from PyQt5 import QtGui
import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

from Controller import Controller
from DailyCasesData import DailyCasesData
from AutoUpdater import AutoUpdater
from CasesUpdateThread import CasesUpdateThread


class CasesTab(qw.QWidget):
    def __init__(self, *args, **kwargs):
        super(CasesTab, self).__init__(*args, **kwargs)

        # VLAKNA
            # auto update vlakno
        self.auto_update_thread = QThread()
        self.auto_update = AutoUpdater(interval=10)
        self.auto_update.moveToThread(self.auto_update_thread)
        self.auto_update_thread.started.connect(self.auto_update.run)
        self.auto_update.update.connect(self.update_fun)
            # update vlakno
        self.update_thread = QThread()
        self.update = CasesUpdateThread()
        self.update.moveToThread(self.update_thread)
        self.update_thread.started.connect(self.update.update_table_data)
        self.update.rows_signal.connect(self.add_rows)
        self.update.rows_signal.connect(self.update_thread.quit)

        self.container = qw.QVBoxLayout()
        self.header = qw.QTableWidget()
        self.table = qw.QTableWidget()
        # Format hlavicky
        self.header.setColumnCount(9)
        self.header.setRowCount(2)
        self.header.horizontalHeader().setVisible(False)
        self.header.verticalHeader().setVisible(False)
        self.header.setEditTriggers(qw.QAbstractItemView.NoEditTriggers)
        self.header.verticalScrollBar().setStyleSheet(open(get_full_path('styles.css')).read())
        self.header.verticalScrollBar().setDisabled(True)
        self.header.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.header.setMinimumHeight(60)
        palette = self.header.palette()
        palette.setBrush(QtGui.QPalette.Highlight, QtGui.QBrush(Qt.lightGray))
        palette.setBrush(QtGui.QPalette.HighlightedText, QtGui.QBrush(Qt.black))
        self.header.setPalette(palette)
        self.header.setFocusPolicy(Qt.NoFocus)
        self.header.setSpan(0, 0, 2, 1)
        self.header.setSpan(0, 1, 1, 2)
        self.header.setSpan(0, 3, 1, 2)
        self.header.setSpan(0, 5, 2, 1)
        self.header.setSpan(0, 6, 2, 1)
        self.header.setSpan(0, 7, 1, 2)
        # Nazvy sloupcu
        header_font = QtGui.QFont('Arial')
        header_font.setPointSize(10)
        header_font.setBold(True)
        cols = [(0, 0, 'Datum'),
                (0, 1, 'Denní přírustek'),
                (0, 3, 'Celkem případů'),
                (0, 5, 'Rozdíl\n(přírustek)'),
                (0, 6, 'Rozdíl\n(celkem)'),
                (0, 7, 'Zpoždění'),
                (1, 1, 'MZ ČR'),
                (1, 2, 'WHO'),
                (1, 3, 'MZ ČR'),
                (1, 4, 'WHO'),
                (1, 7, 'MZ ČR'),
                (1, 8, 'WHO')]
        for (i, j, col) in cols:
            item = qw.QTableWidgetItem(col)
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(Qt.lightGray)
            item.setFont(header_font)
            self.header.setItem(i, j, item)
        # Format tabulky
        self.table.setEditTriggers(qw.QAbstractItemView.NoEditTriggers)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.table.setColumnCount(9)
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setMinimumWidth(790)
        palette = self.table.palette()
        palette.setBrush(QtGui.QPalette.Highlight, QtGui.QBrush(Qt.white))
        palette.setBrush(QtGui.QPalette.HighlightedText, QtGui.QBrush(Qt.black))
        self.table.setPalette(palette)
        self.table.horizontalHeader().setSectionResizeMode(qw.QHeaderView.Stretch)
        self.header.horizontalHeader().setSectionResizeMode(qw.QHeaderView.Stretch)
        # Titulek a tlacitko aktualizace
        self.title_bttn_layout = qw.QHBoxLayout()
        self.title = qw.QLabel('Aktuální situace COVID-19 v ČR (MZ ČR a WHO)')
        self.title.setStyleSheet(open(get_full_path('styles.css')).read())
        self.updated_label = qw.QLabel('Aktualizováno')
        self.hide(self.updated_label)
        self.updated_label.setStyleSheet('margin-right:3px; margin-bottom:10px;')
        self.update_bttn = qw.QPushButton('Aktualizovat data')
        self.update_bttn.clicked.connect(self.update_fun)
        self.update_bttn.setStyleSheet(open(get_full_path('styles.css')).read())
        self.title_bttn_layout.addWidget(self.title, 10)
        self.title_bttn_layout.addWidget(self.updated_label, 1)
        self.title_bttn_layout.addWidget(self.update_bttn, 1)
        self.title_bttn_layout.setAlignment(self.updated_label, Qt.AlignRight)
        self.container.addLayout(self.title_bttn_layout, 1)
        self.container.addWidget(self.header, 1)
        self.container.addWidget(self.table, 10)
        self.container.setSpacing(0)
        self.setLayout(self.container)
        self.auto_update_thread.start()

    def add_rows(self, rows):
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
        self.updated_label.setText('Aktualizováno')
        self.unfade(self.updated_label)
        self.fade(self.updated_label)
        self.update_bttn.setEnabled(True)

    def update_fun(self):
        self.update_thread.start()
        self.update_bttn.setEnabled(False)
        self.updated_label.setText('Aktualizuji...')
        self.unfade(self.updated_label)

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


def get_full_path(file_name):
    """
    Funkce pro získání celé cesty k souboru - vrací celé jméno souboru i s cestou
    """
    file_location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    return os.path.join(file_location, file_name)