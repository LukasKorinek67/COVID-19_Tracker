from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, \
                            QLineEdit, QCompleter
import os


class QuickSearch(QWidget):
    def __init__(self, *args, **kwargs):
        super(QuickSearch, self).__init__(*args, **kwargs)
        self.container = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.countries = open(get_full_path('countries.txt'), encoding='utf-8').read().splitlines()
        self.completer = QCompleter(self.countries)
        self.completer.setCaseSensitivity(0)
        self.search_bar.setCompleter(self.completer)
        self.search_bar.setPlaceholderText('Vybrat zemi')
        self.search_bttn = QPushButton('Přidat')
        self.container.addWidget(self.search_bar)
        self.container.addWidget(self.search_bttn)
        self.setLayout(self.container)

    def text(self):
        return self.search_bar.text()

    def set_default_text(self, text):
        self.search_bar.setText(text)


def get_full_path(file_name):
    """
    Funkce pro získání celé cesty k souboru - vrací celé jméno souboru i s cestou
    """
    file_location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    return os.path.join(file_location, file_name)
