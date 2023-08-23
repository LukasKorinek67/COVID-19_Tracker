#!/bin/env python
# -*- coding: utf-8 -*-

"""
STI - Controller
"""

from datetime import date
from RequestHandler import RequestHandler
from DailyCasesData import DailyCasesData

import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, "database")))
from DatabaseCR import DatabaseCR
from DatabaseVaccination import DatabaseVaccination
from Logger import Logger

name = __name__
log_filename = os.path.join(os.getenv('APPDATA'), 'covidIS_info.log')
logger = Logger()
logger = Logger.init(logger, name, log_filename)


class Controller():
    """
    Třída Controller
    """

    def __init__(self):
        """
        Konstruktor
        """
        self.requestHandler = RequestHandler()
        self.databaseCR = DatabaseCR()
        self.databaseVaccination = DatabaseVaccination()

    def get_cases_data(self):
        """
        - tuto metodu zavolá gui CasesTab při startu aplikace
        - získat data z databáze
        - vrátit je returnem
        """
        try:
            msg = "get_cases_data - SUCCESS"
            logger.info(msg)
            return self.databaseCR.get_info_cr()
        except Exception as e:
            msg = "get_cases_data - ERROR"
            logger.exception(msg)

    def is_data_complete(self, data):
        try:
            if (data is None):
                return False
            elif (data.published_mz is None):
                return False
            elif (data.published_who is None):
                return False
            else:
                return True
            msg = "is_data_complete - SUCCESS"
            logger.info(msg)
        except Exception as e:
            msg = "is_data_complete - ERROR"
            logger.exception(msg)

    def update_cases_data(self):
        """
        - tuto metodu zavolá gui CasesTab při stisknutí tlačítka "Aktualizovat data"
        - získat data z databáze
        - udělat request na dnešní data
        - pokud dnešní data už jsou v databázi tak vrátit null (nic se nezměnilo)
        - pokud ještě nejsou tak uložit do databáze a vrátit je do CasesTab která dnešní data zobrazí na nový řádek
        """
        try:
            today_data_in_database = self.databaseCR.get_today_data()
            # dnešní data z RequestHandleru
            today_data_mz = self.requestHandler.load_mz_data()
            today_data_who = self.requestHandler.load_who_data()

            today = date.today()
            mz_are_today_data = False
            who_are_today_data = False
            if (str(today) == today_data_mz.get("date")):
                mz_are_today_data = True
            if (str(today) == today_data_who.get("date")):
                who_are_today_data = True

            if (mz_are_today_data and who_are_today_data):
                data = DailyCasesData(str(today), today_data_mz.get("published"), today_data_mz.get("daily gain"),
                                      today_data_mz.get("total amount"), today_data_who.get("published"),
                                      today_data_who.get("daily gain"), today_data_who.get("total amount"))
                self.databaseCR.add_info_cr(data)
            elif (mz_are_today_data and not who_are_today_data):
                data = DailyCasesData(str(today), today_data_mz.get("published"), today_data_mz.get("daily gain"),
                                      today_data_mz.get("total amount"), None, None, None)
                self.databaseCR.add_info_cr(data)
            elif (not mz_are_today_data and who_are_today_data):
                data = DailyCasesData(str(today), None, None, None, today_data_who.get("published"),
                                      today_data_who.get("daily gain"), today_data_who.get("total amount"))
                self.databaseCR.add_info_cr(data)
            else:
                data = DailyCasesData(str(today))
                self.databaseCR.add_info_cr(data)
            msg = "update_cases_data - SUCCESS"
            logger.info(msg)
        except Exception as e:
            msg = "update_cases_data - ERROR"
            logger.exception(msg)

    def get_vaccination_data(self):
        """
        - tuto metodu zavolá gui VaccTab při startu aplikace
        - získat data z databáze (zvolených 5 států a jejich data)
        - vrátit je returnem
        """
        try:
            if (self.databaseVaccination.is_database_empty()):
                self.update_vaccination_data()
            msg = "get_vaccination_data - SUCCESS"
            logger.info(msg)
            return self.databaseVaccination.find_chosen_state_vaccination()
        except Exception as e:
            msg = "get_vaccination_data - ERROR"
            logger.exception(msg)

    def update_vaccination_data(self):
        """
        - tuto metodu zavolá gui VaccTab při stisknutí tlačítka "Aktualizovat data"
        - udělat Request na nejnovější data
        - uložit tato data do databáze
        """
        try:
            data = self.requestHandler.load_vaccination_data()
            for state in data:
                self.databaseVaccination.add_info_vaccination(state["name"], str(state["date"]),
                                                              state["percentage vaccinated"], state["last updated"])
            msg = "update_vaccination_data - SUCCESS"
            logger.info(msg)
        except Exception as e:
            msg = "update_vaccination_data - ERROR"
            logger.exception(msg)

    def get_state_vaccination_data(self, state_name, graf_place):
        """
        - tuto metodu zavolá gui VaccTab při vybrání nového státu
        - označit stát jako vybraný - graf_place bude číslo 1-5 podle toho kde je vybraný
        - získat data z databáze a předat je VaccTab
        """
        try:
            if (self.databaseVaccination.is_database_empty()):
                self.update_vaccination_data()
            self.databaseVaccination.update_info_vaccination_chosen(state_name, graf_place)
            msg = "get_state_vaccination_data - SUCCESS"
            logger.info(msg)
            return self.databaseVaccination.find_state_vaccination(state_name)
        except Exception as e:
            msg = "get_state_vaccination_data - ERROR"
            logger.exception(msg)

    def set_state_not_chosen(self, state_name):
        """
        - tuto metodu zavolá gui VaccTab při vybrání nového státu - starý stát určí jako nevybraný
        """
        try:
            self.databaseVaccination.update_info_vaccination_chosen(state_name, 0)
            msg = "set_state_not_chosen - SUCCESS"
            logger.info(msg)
        except Exception as e:
            msg = "set_state_not_chosen - ERROR"
            logger.exception(msg)

    def set_state_chosen(self, state_name, num):
        """
        - tuto metodu zavolá gui VaccTab při vybrání nového státu - starý stát určí jako nevybraný
        """
        try:
            self.databaseVaccination.update_info_vaccination_chosen(state_name, num)
            msg = "set_state_chosen - SUCCESS"
            logger.info(msg)
        except Exception as e:
            msg = "set_state_chosen - ERROR"
            logger.exception(msg)
