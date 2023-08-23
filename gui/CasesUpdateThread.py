from PyQt5.QtCore import QObject, pyqtSignal
import sys
import os

import locale

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

from Controller import Controller


class CasesUpdateThread(QObject):
    rows_signal = pyqtSignal(list)

    def __init__(self):
        super().__init__()

    def update_table_data(self):
        not_loaded_text = "Čeká se"
        controller = Controller()
        controller.update_cases_data()
        data = controller.get_cases_data()
        rows = []
        for day in data:
            row = []
            date = day.date
            czech_date = date[8:10] + "." + date[5:7] + "." + date[0:4]
            row.append(czech_date)
            if day.daily_gain_mz is None:
                row.append(not_loaded_text)
            else:
                locale.setlocale(locale.LC_ALL, '')
                daily_mz = "{0:n}".format(int(day.daily_gain_mz))
                row.append(daily_mz)

            if day.daily_gain_who is None:
                row.append(not_loaded_text)
            else:
                locale.setlocale(locale.LC_ALL, '')
                daily_who = "{0:n}".format(int(day.daily_gain_who))
                row.append(daily_who)

            if day.total_amount_mz is None:
                row.append(not_loaded_text)
            else:
                locale.setlocale(locale.LC_ALL, '')
                total_mz = "{0:n}".format(int(day.total_amount_mz))
                row.append(total_mz)

            if day.total_amount_who is None:
                row.append(not_loaded_text)
            else:
                locale.setlocale(locale.LC_ALL, '')
                total_who = "{0:n}".format(int(day.total_amount_who))
                row.append(total_who)

            if day.diff_daily_gain is None:
                row.append(not_loaded_text)
            else:
                row.append(str(day.diff_daily_gain))

            if day.diff_total_amount is None:
                row.append(not_loaded_text)
            else:
                row.append(str(day.diff_total_amount))

            if day.diff_time is None:
                row.append(not_loaded_text)
                row.append(not_loaded_text)
            else:
                if str(day.diff_time)[0] == "-":
                    row.append("+" + str(day.diff_time))
                    row.append("-" + str(day.diff_time))
                else:
                    row.append("-" + str(day.diff_time))
                    row.append("+" + str(day.diff_time))
            rows.append(row)
        # Po skonceni vrati ziskane radky
        self.rows_signal.emit(rows)